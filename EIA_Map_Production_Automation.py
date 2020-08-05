# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EIA_Map_Production_Automation
                                 A QGIS plugin
 Plugin to automate production of all maps for environmental impact assesments
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-07-21
        git sha              : $Format:%H$
        copyright            : (C) 2020 by WSP
        email                : chris.ryan@wsp.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

#old imports needs tidy

import sys
import os
import processing
import time
import shutil

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.gui import *
from qgis.utils import iface
from PyQt5.QtWidgets import *
from qgis.core import *


# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .EIA_Map_Production_Automation_dialog import EIA_Map_Production_AutomationDialog
import os.path


class EIA_Map_Production_Automation:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'EIA_Map_Production_Automation_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&EIA_Map_Production_Automation')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('EIA_Map_Production_Automation', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/EIA_Map_Production_Automation/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&EIA_Map_Production_Automation'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = EIA_Map_Production_AutomationDialog()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

            # 1.creating sub folders in input project directory

            if result:
                projectfolder = self.dlg.Proj_Folder.text()

                projectGISFolder = projectfolder + "\\" + "EIA Constraints Map Production"
                folders = ["1. Site Location Shapefile", "2.Project Buffers", "3. Clipped Outputs",
                           "4. QGIS Map Docs", "5. Map Outputs"]
            try:
                path = projectGISFolder
                os.makedirs(path, 493)
            except:
                print("error")
            try:
                for folder in folders:
                    path = projectGISFolder + "\\" + folder
                    os.makedirs(path, 493)
            except:
                print("error")


            # ----------------Clipped folder---------------------------------------------------------

            if result:
                Clipped_Sub_Folder = projectGISFolder + "\\" + folders[2] + "\\"
                Sub_Folder = Clipped_Sub_Folder + "\\" + "Clipped Constraints 200m"
                CC_200m = ["Clipped Constraints 200m"]
            try:
                path = Sub_Folder
                os.makedirs(path, 493)
            except:
                print("error")

            if result:
                Clipped_Sub_Folder = projectGISFolder + "\\" + folders[2] + "\\"
                Sub_Folder = Clipped_Sub_Folder + "\\" + "Clipped Constraints 500m"
                CC_500m = ["Clipped Constraints 500m"]
            try:
                path = Sub_Folder
                os.makedirs(path, 493)
            except:
                print("error")
            if result:
                Clipped_Sub_Folder_= projectGISFolder + "\\" + folders[2] + "\\"
                Sub_Folder = Clipped_Sub_Folder + "\\" + "Clipped Constraints 600m"
                CC_600m = ["Clipped Constraints 600m"]
            try:
                path = Sub_Folder
                os.makedirs(path, 493)
            except:
                print("error")
            if result:
                Clipped_Sub_Folder_= projectGISFolder + "\\" + folders[2] + "\\"
                Sub_Folder = Clipped_Sub_Folder + "\\" + "Clipped Constraints 1000m"
                CC_1000m = ["Clipped Constraints 1000m"]
            try:
                path = Sub_Folder
                os.makedirs(path, 493)
            except:
                print("error")
            if result:
                Clipped_Sub_Folder_= projectGISFolder + "\\" + folders[2] + "\\"
                Sub_Folder = Clipped_Sub_Folder + "\\" + "Clipped Constraints 1500m"
                CC_1500m = ["Clipped Constraints 1000m"]
            try:
                path = Sub_Folder
                os.makedirs(path, 493)
            except:
                print("error")
            if result:
                Clipped_Sub_Folder_= projectGISFolder + "\\" + folders[2] + "\\"
                Sub_Folder = Clipped_Sub_Folder + "\\" + "Clipped Constraints 2000m"
                CC_2000m = ["Clipped Constraints 2000m"]
            try:
                path = Sub_Folder
                os.makedirs(path, 493)
            except:
                print("error")

           #--------------------------------------------------------------------------------

            # creating buffers

            Buffer_Folder = projectGISFolder + "\\" + folders[1] + "\\"

            Buff200 = Buffer_Folder + "\\" + "Site Location 200m Buffer.shp"
            Buff500 = Buffer_Folder + "\\" + "Site Location 500m Buffer.shp"
            Buff600 = Buffer_Folder + "\\" + "Site Location 600m Buffer.shp"
            Buff1000 = Buffer_Folder + "\\" + "Site Location 1000m Buffer.shp"
            Buff1500 = Buffer_Folder + "\\" + "Site Location 1500m Buffer.shp"
            Buff2000 = Buffer_Folder + "\\" + "Site Location 2000m Buffer.shp"


            processing.run("native:buffer",
                           {'INPUT': 'E:\\EIA\\Data\\Mock centerline\\Mock_centerline.shp', 'DISTANCE': 200,
                            'SEGMENTS': 5, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': True,
                            'OUTPUT': Buff200})
            processing.run("native:buffer",
                           {'INPUT': 'E:\\EIA\\Data\\Mock centerline\\Mock_centerline.shp', 'DISTANCE': 500,
                            'SEGMENTS': 5, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': True,
                            'OUTPUT': Buff500})
            processing.run("native:buffer",
                           {'INPUT': 'E:\\EIA\\Data\\Mock centerline\\Mock_centerline.shp', 'DISTANCE': 600,
                            'SEGMENTS': 5, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': True,
                            'OUTPUT': Buff600})
            processing.run("native:buffer",
                           {'INPUT': 'E:\\EIA\\Data\\Mock centerline\\Mock_centerline.shp', 'DISTANCE': 1000,
                            'SEGMENTS': 5, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': True,
                            'OUTPUT': Buff1000})
            processing.run("native:buffer",
                           {'INPUT': 'E:\\EIA\\Data\\Mock centerline\\Mock_centerline.shp', 'DISTANCE': 1500,
                            'SEGMENTS': 5, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': True,
                            'OUTPUT': Buff1500})
            processing.run("native:buffer",
                           {'INPUT': 'E:\\EIA\\Data\\Mock centerline\\Mock_centerline.shp', 'DISTANCE': 2000,
                            'SEGMENTS': 5, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': True,
                            'OUTPUT': Buff2000})

            #reprojecting Buffers

            Buff200_WGS = Buffer_Folder + "\\" + "Site Location 200m Buffer WGS.shp"
            Buff500_WGS= Buffer_Folder + "\\" + "Site Location 500m Buffer WGS.shp"
            Buff600_WGS = Buffer_Folder + "\\" + "Site Location 600m Buffer WGS .shp"
            Buff1000_WGS = Buffer_Folder + "\\" + "Site Location 1000m Buffer WGS.shp"
            Buff1500_WGS = Buffer_Folder + "\\" + "Site Location 1500m Buffer WGS.shp"
            Buff2000_WGS = Buffer_Folder + "\\" + "Site Location 2000m Buffer WGS.shp"

            processing.run("native:reprojectlayer", {
                'INPUT': Buff200,
                'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:3857'), 'OUTPUT': Buff200_WGS})
            processing.run("native:reprojectlayer", {
                'INPUT': Buff500,
                'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:3857'), 'OUTPUT': Buff500_WGS})
            processing.run("native:reprojectlayer", {
                'INPUT': Buff600,
                'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:3857'), 'OUTPUT': Buff600_WGS})
            processing.run("native:reprojectlayer", {
                'INPUT': Buff1000,
                'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:3857'), 'OUTPUT': Buff1000_WGS})
            processing.run("native:reprojectlayer", {
                'INPUT': Buff1500,
                'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:3857'), 'OUTPUT': Buff1500_WGS})


            # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # Clipping Layers to buffers

            clip_output_200m = Clipped_Sub_Folder + "\\" + CC_200m[0] + "\\"
            clip_output_500m = Clipped_Sub_Folder + "\\" + CC_500m[0] + "\\"
            clip_output_600m = Clipped_Sub_Folder + "\\" + CC_600m[0] + "\\"
            clip_output_1km = Clipped_Sub_Folder + "\\" + CC_1000m[0] + "\\"
            clip_output_1_5km = Clipped_Sub_Folder + "\\" + CC_1500m[0] + "\\"
            clip_output_2km = Clipped_Sub_Folder + "\\" + CC_2000m[0] + "\\"


            EIA_Data = r'\\uk.wspgroup.com\central data\Discipline Management\Development\01 Service Lines\Smart Consulting\Digital\Data & Analysis\EIA Datastore\Test Constraints data' + "\\"


            # Clipping Constraints to buffer distances:

            datalist = []
            for item in os.listdir(EIA_Data):
                if item[-3:] == 'shp':
                    datalist.append(item)

            for layer in datalist:
                processing.run("native:clip",
                               {'INPUT': EIA_Data + layer,
                                'OVERLAY': Buff200,
                                'OUTPUT': clip_output_200m + layer})
                processing.run("native:clip",
                               {'INPUT': EIA_Data + "\\" + layer,
                                'OVERLAY': Buff500,
                                'OUTPUT': clip_output_500m + layer})
                processing.run("native:clip",
                               {'INPUT': EIA_Data + "\\" + layer,
                                'OVERLAY': Buff600,
                                'OUTPUT': clip_output_600m + layer})
                processing.run("native:clip",
                               {'INPUT': EIA_Data + "\\" + layer,
                                'OVERLAY': Buff1000,
                                'OUTPUT': clip_output_1km + layer})
                processing.run("native:clip",
                               {'INPUT': EIA_Data + "\\" + layer,
                                'OVERLAY': Buff1500,
                                'OUTPUT': clip_output_1_5km + layer})
                processing.run("native:clip",
                               {'INPUT': EIA_Data + "\\" + layer,
                                'OVERLAY': Buff2000,
                                'OUTPUT': clip_output_2km + layer})


           #-----------------------------------------------------------------------------------------------------------------------------------------------------

            # importing symbology into output shapefile folders:
            main_symbol_folder = r'\\uk.wspgroup.com\central data\Discipline Management\Development\01 Service Lines\Smart Consulting\Digital\Data & Analysis\EIA Datastore\QML Symbols'
            main_symbols_list = []
            for symbols in os.listdir(main_symbol_folder):
                if symbols[-3:] == 'qml':
                    main_symbols_list.append(main_symbol_folder + "\\" + symbols)
            for ms in main_symbols_list:
                shutil.copy(ms, clip_output_200m),
                shutil.copy(ms, clip_output_500m),
                shutil.copy(ms, clip_output_600m),
                shutil.copy(ms, clip_output_1km),
                shutil.copy(ms, clip_output_1_5km),
                shutil.copy(ms, clip_output_2km),


            # ---Map names ----------------------------------------------------------
            Map1name = "Map 1 - Site Location Plan.qgs"
            Map2name = "Map 2"
            Map3name = "Map 3 "

            # ----------Creating Map 1----------------------------------------------------------------------------------------

            Mapout = projectGISFolder + "\\" + folders[3] + "\\"
            project1 = QgsProject.instance()
            project1.setCrs(QgsCoordinateReferenceSystem(3857))
            project1.setFileName(Mapout + Map1name)

            mapbox_basemap = 'type=xyz&url=https://api.mapbox.com/styles/v1/chris-ryan-wsp/ck3r54pn8041b1cmzvdaxv1qc/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiY2hyaXMtcnlhbi13c3AiLCJhIjoiY2szazRzNnhqMG8xZTNjb2N5NDVqeTV5MSJ9.hpX0Il1EIUT5pc7v-Z7lSQ'
            rlayer = QgsRasterLayer(mapbox_basemap, 'Mapbox', 'wms')
            QgsProject.instance().addMapLayer(rlayer)

            shplayer = iface.addVectorLayer(Buff1000_WGS, "", "ogr")
            shplayer.setCrs(QgsCoordinateReferenceSystem(3857))
            project1.addMapLayer(shplayer)

            vlayer = shplayer
            settings = QgsMapSettings()
            settings.setLayers([vlayer])
            settings.setExtent(vlayer.extent())






            #removes empty layers from layer list - not needed on map outputs

            Layermap = QgsProject.instance().mapLayers()
            RemoveLayers = []
            for name, layer in Layermap.items():
                if layer.isValid():
                    if layer.type() == QgsMapLayer.VectorLayer:
                        if layer.featureCount() == 0:
                            RemoveLayers.append(layer.id())
            if len(RemoveLayers) > 0:
                QgsProject.instance().removeMapLayers(RemoveLayers)






            # ------create map item in the layout_---------------------------------------------------------------------------------------------


            project = QgsProject.instance()
            manager = project.layoutManager()
            layoutName = 'Map 1: Site Location Plan'
            layouts_list = manager.printLayouts()

            # removes dublicate layers produced
            for layout in layouts_list:
                if layout.name() == layoutName:
                    manager.removeLayout(layout)

            layout = QgsPrintLayout(project)
            layout.initializeDefaults()
            layout.setName(layoutName)

            manager.addLayout(layout)
            canvas = iface.mapCanvas()

            # Creating a frame around map and legend - min/max in mm in layout
            xmin = 5
            xmax = 292
            ymin = 2
            ymax = 208
            polygon = QPolygonF()
            polygon.append(QPointF(xmin, ymin))
            polygon.append(QPointF(xmax, ymin))
            polygon.append(QPointF(xmax, ymax))
            polygon.append(QPointF(xmin, ymax))

            # Create the polygon from nodes
            polygonItem = QgsLayoutItemPolygon(polygon, layout)

            # Add to the layout
            layout.addItem(polygonItem)

            # adding map to layout
            Map = QgsLayoutItemMap.create(layout)
            Map.setRect(10, 10, 210, 90)
            ms = QgsMapSettings()
            #ms.setLayers([layer1])
            Map.setFrameEnabled(True)
            Map.setExtent(canvas.extent())
            Map.setScale(80000, forceUpdate=1)

            layout.addLayoutItem(Map)

            Map.attemptMove(QgsLayoutPoint(4, 2, QgsUnitTypes.LayoutMillimeters))
            # ============================(Width, Length)
            Map.attemptResize(QgsLayoutSize(215, 206, QgsUnitTypes.LayoutMillimeters))

            # addding custom arrow
            picture2 = QgsLayoutItemPicture(layout)
            picture2.update()
            layout.addLayoutItem(picture2)
            picture2.setPicturePath(
                r"\\uk.wspgroup.com\central data\Discipline Management\Development\01 Service Lines\Smart Consulting\Digital\Data & Analysis\Active Travel Zones\Map Template Items\NorthArrow_Red.png")
            picture2.attemptMove(QgsLayoutPoint(5, 3, QgsUnitTypes.LayoutMillimeters))
            picture2.setResizeMode(QgsLayoutItemPicture.FrameToImageSize)

            # adding scalebar
            scalebar = QgsLayoutItemScaleBar(layout)
            scalebar.setStyle('Single Box')
            scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
            scalebar.setNumberOfSegments(3)
            scalebar.setNumberOfSegmentsLeft(0)
            scalebar.setUnitsPerSegment(1)
            scalebar.setLinkedMap(Map)
            scalebar.setUnitLabel('km')
            scalebar.setFont(QFont('Arial', 8))
            scalebar.refresh()
            layout.addLayoutItem(scalebar)
            # ============================------(Width, Length)
            scalebar.attemptMove(QgsLayoutPoint(148, 196, QgsUnitTypes.LayoutMillimeters))
            scalebar.applyDefaultSize
            scalebar.refresh()

            # adding title
            title = QgsLayoutItemLabel(layout)
            title.setBackgroundEnabled(True)
            title.setText('Map 1: Site Location Plan')
            title.setFont(QFont('Arial', 20))
            title.setFontColor(QColor('red'))
            title.adjustSizeToText()
            layout.addLayoutItem(title)
            # ============================---(Width, Length)
            title.attemptMove(QgsLayoutPoint(82, 3, QgsUnitTypes.LayoutMillimeters))
            title.refresh()

            # adding WSP logo
            picture = QgsLayoutItemPicture(layout)
            picture.update()
            layout.addLayoutItem(picture)
            picture.setPicturePath(
                r"\\uk.wspgroup.com\central data\Discipline Management\Development\01 Service Lines\Smart Consulting\Digital\Data & Analysis\Active Travel Zones\Map Template Items\wsp_logo.png")
            picture.attemptMove(QgsLayoutPoint(5, 195, QgsUnitTypes.LayoutMillimeters))
            picture.setResizeMode(QgsLayoutItemPicture.FrameToImageSize)

            # adding legend and layers into legend
            legend = QgsLayoutItemLegend(layout)
            legend.setLinkedMap(Map)
            legend.refresh()
            layouts_check = QgsProject.instance().layoutManager()
            legend.setTitle("Key:")
            newFont = QFont("Aerial", 8)
            LargeFont = QFont("Aerial", 12)
            legend.setStyleFont(QgsLegendStyle.Title, LargeFont)
            legend.setStyleFont(QgsLegendStyle.Subgroup, newFont)
            legend.setStyleFont(QgsLegendStyle.SymbolLabel, newFont)
            layout.addLayoutItem(legend)

            # ============================---(Width, Length)
            legend.attemptMove(QgsLayoutPoint(221, 4, QgsUnitTypes.LayoutMillimeters))
            legend.attemptResize(QgsLayoutSize(15, QgsUnitTypes.LayoutMillimeters))
            legend.refresh()

            # ----- Export map as PDF and PNG--------------------------------

            OutMaps = projectGISFolder + "\\" + folders[4] + "\\"
            fn = OutMaps + "Map 1 - Site Location Plan.png"
            exporter = QgsLayoutExporter(layout)
            exporter.exportToImage(fn, QgsLayoutExporter.ImageExportSettings())

            # ------Map 1 completed---------------------

            # layout.refresh()
            project1.write()
            project1.clear()

