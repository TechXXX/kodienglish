# -*- coding: utf-8 -*-
import xbmc, xbmcgui
import json
from threading import Thread

pause_services_prop = 'fenlight.pause_services'
firstrun_update_prop = 'fenlight.firstrun_update'
current_skin_prop = 'fenlight.current_skin'
trakt_service_string = 'TraktMonitor Service Update %s - %s'
trakt_success_line_dict = {'success': 'Trakt Update Performed', 'no account': '(Unauthorized) Trakt Update Performed'}
update_string = 'Next Update in %s minutes...'
old_trakt_client_id = '1038ef327e86e7f6d39d80d2eb5479bff66dd8394e813c5e0e387af0f84d89fb'

def logger(heading, function):
	xbmc.log('###%s###: %s' % (heading, function), 1)

class SetAddonConstants:
	def run(self):
		logger('Fen Light', 'SetAddonConstants Service Starting')
		import xbmcgui, xbmcaddon, xbmcvfs
		addon_object = xbmcaddon.Addon('plugin.video.fenlight.kodienglish')
		self.window = xbmcgui.Window(10000)
		_info = addon_object.getAddonInfo
		addon_items = [('fenlight.addon_version', _info('version')),
					('fenlight.addon_path', _info('path')),
					('fenlight.addon_profile', xbmcvfs.translatePath(_info('profile'))),
					('fenlight.addon_icon', xbmcvfs.translatePath(_info('icon'))),
					('fenlight.addon_fanart', xbmcvfs.translatePath(_info('fanart')))]
		for item in addon_items: self.set_property(*item)
		return logger('Fen Light', 'SetAddonConstants Service Finished')

	def set_property(self, prop, value):
		self.window.setProperty(prop, value)

class DatabaseMaintenance:
	def run(self):
		logger('Fen Light', 'DatabaseMaintenance Service Starting')
		from caches.base_cache import make_databases
		make_databases()
		return logger('Fen Light', 'DatabaseMaintenance Service Finished')

class SyncSettings:
	def run(self):
		logger('Fen Light', 'SyncSettings Service Starting')
		from caches.settings_cache import sync_settings
		sync_settings()
		try:
			from apis.trakt_api import sync_trakt_auth_state
			sync_trakt_auth_state()
		except: pass
		logger('Fen Light', 'SyncSettings Service Finished')

class OnUpdateChanges:
	def run(self):
		logger('Fen Light', 'OnUpdateChanges Service Starting')
		from caches.settings_cache import get_setting, set_setting
		try:
			migrations = (
				('refresh_addon_keys', self.refresh_addon_keys),
				('enable_torbox_cloud_search', self.enable_torbox_cloud_search),
				('migrate_external_scraper_to_magneto', self.migrate_external_scraper_to_magneto),
				('set_magneto_provider_selection', self.set_magneto_provider_selection),
			)
			for setting_id, migration in migrations:
				update_setting_id = 'updatechecks.%s' % setting_id
				if get_setting('fenlight.%s' % update_setting_id, 'false') == 'true': continue
				migration()
				set_setting(update_setting_id, 'true')
		except Exception as e:
			logger('Fen Light', 'OnUpdateChanges Service Failed: %s' % str(e))
		return logger('Fen Light', 'OnUpdateChanges Service Finished')

	def refresh_addon_keys(self):
		from caches.settings_cache import get_setting, set_setting, restore_setting_default
		current_trakt_client = (get_setting('fenlight.trakt.client') or '').lower()
		if current_trakt_client != old_trakt_client_id: return
		from caches.trakt_cache import clear_all_trakt_cache_data
		from modules import kodi_utils
		restore_setting_default({'silent': 'true', 'setting_id': 'trakt.client'})
		restore_setting_default({'silent': 'true', 'setting_id': 'trakt.secret'})
		setting_resets = (
			('trakt.user', 'empty_setting'),
			('trakt.expires', ''),
			('trakt.token', ''),
			('trakt.refresh', ''),
			('trakt.next_daily_clear', '0'),
			('trakt.auth_state', 'not_authorized'),
			('trakt.auth_state_display_name', 'Not Authorized'),
			('watched_indicators', '0'),
		)
		for setting_id, value in setting_resets:
			set_setting(setting_id, value)
		clear_all_trakt_cache_data(silent=True, refresh=False)
		logger('Fen Light', 'Old Trakt client ID detected. Trakt credentials reset; reauthorization required.')
		kodi_utils.ok_dialog(
			heading='Trakt Credentials Reset',
			text='Fen Light English has replaced an old Trakt app key with the current default.[CR][CR]Please re-authorize your Trakt account.'
		)

	def enable_torbox_cloud_search(self):
		from caches.settings_cache import set_setting
		set_setting('provider.tb_cloud', 'true')
		logger('Fen Light', 'TorBox cloud storage search enabled for Fen Light English.')

	def migrate_external_scraper_to_magneto(self):
		from caches.settings_cache import get_setting, set_setting
		current_module = get_setting('fenlight.external_scraper.module', '')
		if current_module != 'script.module.cocoscrapers': return
		try:
			import xbmcaddon
			xbmcaddon.Addon('script.module.magneto')
		except Exception as e:
			raise Exception('Magneto module unavailable: %s' % str(e))
		self.apply_magneto_provider_defaults()
		self.sync_magneto_undesirables_from_coco()
		set_setting('external_scraper.module', 'script.module.magneto')
		set_setting('external_scraper.name', 'Magneto Module')
		set_setting('provider.external', 'true')
		logger('Fen Light', 'External scraper migrated from CocoScrapers to Magneto for Fen Light English.')

	def apply_magneto_provider_defaults(self):
		try:
			import os, xbmcaddon, xml.etree.ElementTree as ET
			magneto_addon = xbmcaddon.Addon('script.module.magneto')
			settings_path = os.path.join(magneto_addon.getAddonInfo('path'), 'resources', 'settings.xml')
			settings_root = ET.parse(settings_path).getroot()
			provider_defaults = []
			for item in settings_root.iter('setting'):
				setting_id = item.attrib.get('id', '')
				setting_default = item.attrib.get('default')
				if setting_id.startswith('provider.') and setting_default in ('true', 'false'):
					provider_defaults.append((setting_id, setting_default))
			for setting_id, setting_default in provider_defaults:
				magneto_addon.setSetting(setting_id, setting_default)
			logger('Fen Light', 'Applied %s Magneto provider defaults for Fen Light English.' % len(provider_defaults))
		except Exception as e:
			logger('Fen Light', 'Magneto provider defaults sync failed: %s' % str(e))

	def set_magneto_provider_selection(self):
		from caches.settings_cache import get_setting
		if get_setting('fenlight.external_scraper.module', '') != 'script.module.magneto': return
		import os, xbmcaddon, xml.etree.ElementTree as ET
		enabled_providers = ('provider.comet', 'provider.mediafusion', 'provider.torrentio')
		magneto_addon = xbmcaddon.Addon('script.module.magneto')
		settings_path = os.path.join(magneto_addon.getAddonInfo('path'), 'resources', 'settings.xml')
		settings_root = ET.parse(settings_path).getroot()
		provider_settings = []
		for item in settings_root.iter('setting'):
			setting_id = item.attrib.get('id', '')
			if setting_id.startswith('provider.'): provider_settings.append(setting_id)
		for setting_id in provider_settings:
			magneto_addon.setSetting(setting_id, 'true' if setting_id in enabled_providers else 'false')
		logger('Fen Light', 'Enabled preferred Magneto providers for Fen Light English: %s' % ', '.join(enabled_providers))

	def sync_magneto_undesirables_from_coco(self):
		coco_settings = {
			'filter.undesirables': 'true',
			'filter.foreign.single.audio': 'true'
		}
		try:
			import xbmcaddon
			try:
				coco_addon = xbmcaddon.Addon('script.module.cocoscrapers')
				for setting_id in coco_settings:
					value = coco_addon.getSetting(setting_id)
					if value in ('true', 'false'): coco_settings[setting_id] = value
			except Exception as e:
				logger('Fen Light', 'CocoScrapers undesirables settings unavailable; using Coco defaults: %s' % str(e))
			magneto_addon = xbmcaddon.Addon('script.module.magneto')
			for setting_id, value in coco_settings.items():
				magneto_addon.setSetting(setting_id, value)
		except Exception as e:
			logger('Fen Light', 'Magneto undesirables settings sync failed: %s' % str(e))
		try:
			self.merge_magneto_undesirables_database()
		except Exception as e:
			logger('Fen Light', 'Magneto undesirables database sync failed: %s' % str(e))

	def merge_magneto_undesirables_database(self):
		import os, sqlite3, xbmcvfs
		profile_path = xbmcvfs.translatePath('special://profile/addon_data')
		coco_db = os.path.join(profile_path, 'script.module.cocoscrapers', 'undesirables.db')
		magneto_profile = os.path.join(profile_path, 'script.module.magneto')
		magneto_db = os.path.join(magneto_profile, 'undesirables.db')
		if not os.path.exists(coco_db): return
		if not os.path.exists(magneto_profile): os.makedirs(magneto_profile)
		with sqlite3.connect(coco_db) as coco_con:
			rows = coco_con.execute('SELECT keyword, user_defined, enabled FROM undesirables').fetchall()
		if not rows: return
		with sqlite3.connect(magneto_db) as magneto_con:
			magneto_con.execute('CREATE TABLE IF NOT EXISTS undesirables (keyword TEXT NOT NULL, user_defined BOOL NOT NULL, enabled BOOL NOT NULL, UNIQUE(keyword))')
			magneto_con.executemany('INSERT OR REPLACE INTO undesirables VALUES (?, ?, ?)', rows)
			magneto_con.commit()
		logger('Fen Light', 'Copied %s CocoScrapers undesirables entries to Magneto for Fen Light English.' % len(rows))

class CustomFonts:
	def run(self):
		logger('Fen Light', 'CustomFonts Service Starting')
		from windows.base_window import FontUtils
		monitor, player, window = xbmc.Monitor(), xbmc.Player(), xbmcgui.Window(10000)
		wait_for_abort, is_playing = monitor.waitForAbort, player.isPlayingVideo
		window.clearProperty(current_skin_prop)
		font_utils = FontUtils()
		while not monitor.abortRequested():
			font_utils.execute_custom_fonts()
			if window.getProperty(pause_services_prop) == 'true' or is_playing(): sleep = 20
			else: sleep = 10
			wait_for_abort(sleep)
		try: del monitor
		except: pass
		try: del player
		except: pass
		return logger('Fen Light', 'CustomFonts Service Finished')

class TraktMonitor:
	def run(self):
		logger('Fen Light', 'TraktMonitor Service Starting')
		from apis.trakt_api import trakt_sync_activities
		from caches.settings_cache import get_setting
		from modules.kodi_utils import run_plugin
		from modules.settings import trakt_sync_interval
		monitor, player, window = xbmc.Monitor(), xbmc.Player(), xbmcgui.Window(10000)
		wait_for_abort, is_playing = monitor.waitForAbort, player.isPlayingVideo
		while not monitor.abortRequested():
			while is_playing() or window.getProperty(pause_services_prop) == 'true': wait_for_abort(10)
			wait_time = 1800
			try:
				sync_interval, wait_time = trakt_sync_interval()
				next_update_string = update_string % sync_interval
				status = trakt_sync_activities()
				if status == 'failed': logger('Fen Light', trakt_service_string % ('Failed. Error from Trakt', next_update_string))
				else:
					if status in ('success', 'no account'): logger('Fen Light', trakt_service_string % ('Success. %s' % trakt_success_line_dict[status], next_update_string))
					else: logger('Fen Light', trakt_service_string % ('Success. No Changes Needed', next_update_string))# 'not needed'
					if status == 'success' and get_setting('fenlight.trakt.refresh_widgets', 'false') == 'true': run_plugin({'mode': 'kodi_refresh'})
			except Exception as e: logger('Fen Light', trakt_service_string % ('Failed', 'The following Error Occured: %s' % str(e)))
			wait_for_abort(wait_time)
		try: del monitor
		except: pass
		try: del player
		except: pass
		return logger('Fen Light', 'TraktMonitor Service Finished')

class UpdateCheck:
	def run(self):
		window = xbmcgui.Window(10000)
		if window.getProperty(firstrun_update_prop) == 'true': return
		logger('Fen Light', 'UpdateCheck Service Starting')
		from time import time
		from modules.updater import update_check
		from modules.settings import update_action, update_delay
		end_pause = time() + update_delay()
		monitor, player = xbmc.Monitor(), xbmc.Player()
		wait_for_abort, is_playing = monitor.waitForAbort, player.isPlayingVideo
		while not monitor.abortRequested():
			while time() < end_pause: wait_for_abort(1)
			while window.getProperty(pause_services_prop) == 'true' or is_playing(): wait_for_abort(1)
			update_check(update_action())
			break
		window.setProperty(firstrun_update_prop, 'true')
		try: del monitor
		except: pass
		try: del player
		except: pass
		return logger('Fen Light', 'UpdateCheck Service Finished')

class WidgetRefresher:
	def run(self):
		logger('Fen Light', 'WidgetRefresher Service Starting')
		from time import time
		from caches.settings_cache import get_setting
		from modules.kodi_utils import home, run_plugin
		monitor, player = xbmc.Monitor(), xbmc.Player()
		wait_for_abort, self.is_playing = monitor.waitForAbort, player.isPlayingVideo
		self.window = xbmcgui.Window(10000)
		self.get_setting = get_setting
		self.home = home
		self.window.setProperty('fenlight.refresh_widgets', 'true')
		self.set_next_refresh(time())
		wait_for_abort(20)
		while not monitor.abortRequested():
			try:
				wait_for_abort(10)
				self.window.clearProperty('fenlight.refresh_widgets')
				offset = int(self.get_setting('fenlight.widget_refresh_timer', '60'))
				if offset != self.offset:
					self.set_next_refresh(time())
					continue
				if self.condition_check(): continue
				if self.next_refresh < time():
					run_plugin({'mode': 'refresh_widgets', 'show_notification': self.get_setting('fenlight.widget_refresh_notification', 'false')}, block=True)
					logger('Fen Light', 'WidgetRefresher Service - Widgets Refreshed')
					self.set_next_refresh(time())
			except: pass
		try: del monitor
		except: pass
		try: del player
		except: pass
		return logger('Fen Light', 'WidgetRefresher Service Finished')

	def condition_check(self):
		if not self.home(): return True
		if self.next_refresh == None or self.is_playing() or self.window.getProperty(pause_services_prop) == 'true': return True
		if self.window.getProperty('fenlight.window_loaded') == 'true': return True 
		try:
			window_stack = json.loads(self.window.getProperty('fenlight.window_stack'))
			if window_stack or window_stack == []: return True
		except: pass
		return False

	def set_next_refresh(self, _time):
		self.offset = int(self.get_setting('fenlight.widget_refresh_timer', '60'))
		if self.offset: self.next_refresh = _time + (self.offset*60)
		else: self.next_refresh = None

class AutoStart:
	def run(self):
		logger('Fen Light', 'AutoStart Service Starting')
		from modules.settings import auto_start_fenlight
		if auto_start_fenlight():
			from modules.kodi_utils import run_addon
			run_addon()
		return logger('Fen Light', 'AutoStart Service Finished')

class FenLightMonitor(xbmc.Monitor):
	def __init__ (self):
		xbmc.Monitor.__init__(self)
		self.startServices()

	def startServices(self):
		SetAddonConstants().run()
		DatabaseMaintenance().run()
		SyncSettings().run()
		OnUpdateChanges().run()
		Thread(target=CustomFonts().run).start()
		Thread(target=TraktMonitor().run).start()
		Thread(target=UpdateCheck().run).start()
		Thread(target=WidgetRefresher().run).start()
		AutoStart().run()

	def onNotification(self, sender, method, data):
		if method in ('GUI.OnScreensaverActivated', 'System.OnSleep'):
			xbmcgui.Window(10000).setProperty(pause_services_prop, 'true')
			logger('OnNotificationActions', 'PAUSING Fen Light Services Due to Device Sleep')
		elif method in ('GUI.OnScreensaverDeactivated', 'System.OnWake'):
			xbmcgui.Window(10000).clearProperty(pause_services_prop)
			logger('OnNotificationActions', 'UNPAUSING Fen Light Services Due to Device Awake')

logger('Fen Light', 'Main Monitor Service Starting')
FenLightMonitor().waitForAbort()
logger('Fen Light', 'Main Monitor Service Finished')
