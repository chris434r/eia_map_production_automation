# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EIA_Map_Production_Automation
                                 A QGIS plugin
 Plugin to automate production of all maps for environmental impact assesments
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-07-21
        copyright            : (C) 2020 by WSP
        email                : chris.ryan@wsp.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load EIA_Map_Production_Automation class from file EIA_Map_Production_Automation.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .EIA_Map_Production_Automation import EIA_Map_Production_Automation
    return EIA_Map_Production_Automation(iface)
