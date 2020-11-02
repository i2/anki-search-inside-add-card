from aqt import QMenu, mw
from aqt.qt import QAction, QKeySequence
from .config import get_config_value
from aqt.utils import showInfo
from .dialogs.editor import open_editor, NoteEditor
from .dialogs.queue_picker import QueuePicker
from .dialogs.quick_open_pdf import QuickOpenPDF
from .dialogs.zotero_import import ZoteroImporter
from .dialogs.settings import SettingsDialog

class Menu():
    def __init__(self):
        menu_name = "test"
        menu = self.get_menu(mw, "&SIAC")

        submenu_import = self.get_sub_menu(menu, "Import")

        import_options=( #SHORTCUT_CONF_KEY, TITLE, CALLBACK
            ("shortcuts.menubar.import.create_new", "New",           self.import_create_new),
            #("shortcuts.menubar.import.youtube",    "YouTube",       self.import_youtube), # still dysfunctional
            ("shortcuts.menubar.import.zotero_csv", "Zotero CSV",    self.import_zotero)
        )

        self.add_menu_actions(submenu_import, import_options)

        menu_options=( # CONF_KEY, TITLE, CALLBACK
            ("shortcuts.menubar.queue_manager",  "Queue Manager",    self.queue_manager), # somewhat functional
            #("shortcuts.menubar.quick_open",     "Quick Open...",    self.quick_open), # still dysfunctional
            ("shortcuts.menubar.addon_settings", "Add-On Settings",  self.settings)
        )

        self.add_menu_actions(menu, menu_options)

    # Import -> Zotero
    def import_zotero(self):
        dialog = ZoteroImporter(mw.app.activeWindow())

        if dialog.exec_():
            tooltip(f"Created {dialog.total_count} notes.")

    # Import -> New
    def import_create_new(self):
        dialog = NoteEditor(mw.app.activeWindow())

    # Import -> Youtube
    # def import_youtube(self):
    #    dialog = ZoteroImporter(mw.app.activeWindow())

    # def quick_open(self):
    #    dialog = QuickOpenPDF(mw.app.activeWindow())

    def queue_manager(self):
        dialog = QueuePicker(mw.app.activeWindow())

    def settings(self):
        dialog = SettingsDialog(mw.app.activeWindow())

    # Menu bar settings
    def get_menu(self, parent, menuName):
        menubar = parent.form.menubar
        for a in menubar.actions():
            if menuName == a.text():
                return a.menu()
        else:
            return menubar.addMenu(menuName)


    def get_sub_menu(self, menu, subMenuName):
        for a in menu.actions():
            if subMenuName == a.text():
                return a.menu()
        else:
            subMenu = QMenu(subMenuName, menu)
            menu.addMenu(subMenu)
            return subMenu

    def add_menu_actions(self, menu, menu_options):
        for k,t,cb in menu_options:
            hk = 0
            if k:
                hk = get_config_value(k)

            act = QAction(t,menu)
            if hk:
                act.setShortcut(QKeySequence(hk))

            act.triggered.connect(cb)
            menu.addAction(act)
