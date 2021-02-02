# -*- coding: utf-8 -*-

"""
/***************************************************************************
 MultiMapLayout
                                 A QGIS plugin
 MultiMapLayout
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-01-28
        copyright            : (C) 2021 by Giulio Fattori
        email                : giulio.fattori@tin.it
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

__author__ = 'Giulio Fattori'
__date__ = '2021-01-28'
__copyright__ = '(C) 2021 by Giulio Fattori'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtWidgets import QAction 
from PyQt5.QtGui import QFont, QColor
from qgis.utils import iface
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (Qgis,
                       #QgsField,
                       #QgsFields,
                       #QgsWkbTypes,
                       QgsExpression,
                       QgsProject,
                       QgsPrintLayout,
                       QgsLayoutPoint,
                       QgsLayoutSize,
                       QgsUnitTypes,
                       QgsTextFormat,
                       QgsLayoutItemPage,
                       QgsLayoutItemMap,
                       QgsLayoutItemLabel,
                       QgsLayoutMeasurement,
                       QgsLayoutItemScaleBar,
                       QgsMapSettings,
                       #QgsMapRendererParallelJob,
                       QgsLayoutExporter,
                       #QgsFeature,
                       QgsGeometry,
                       QgsRectangle,
                       QgsProcessing,
                       QgsFeatureSink,
                       QgsLayerTreeGroup,
                       QgsLayerTreeLayer,
                       QgsProcessingParameterExpression,
                       QgsProcessingParameterString,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterExtent,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFileDestination)
                       
from qgis import processing
import math

#questo per l'icona dell'algoritmo di processing
import os
import inspect
from qgis.PyQt.QtGui import QIcon

class MultiMapLayoutAlgorithm(QgsProcessingAlgorithm):

# Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    PAPER_DIM = 'PAPER_DIM'    #dimensione carta
    PAPER_ORI = 'PAPER_ORI'    #orientamento
    COLON_NUM = 'COLON_NUM'    #numero di colonne
    INPUT_LYR = 'INPUT_LYR'    #layer in sequenza
    INPUT_EXT = 'INPUT_EXT'    #input extension
    INPUT_SCL = 'INPUT_SCL'    #input extension
    INPUT_TIT = 'INPUT_TIT'    #input composition title
    INPUT_EXP = 'INPUT_EXP'    #input espressione
    
    OUTPUT_PDF = 'OUTPUT_PDF'  #pdf in uscita
    OUTPUT = 'OUTPUT'
    

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ComposerMultiMapProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'MultiMap layout from layers'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('MultiMap layout from layers')
    
    #icona dell'algoritmo di processing
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'multimap.svg')))
        return icon
    
    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr(
        "<p><mark style='color:green'><strong>Layout di stampa con mappe multiple su singolo foglio\n\
        <mark style='color:blue'><strong>OPZIONI</strong></mark>\n\
        <mark style='color:black'>- Titolo composizione</mark>\n\
        <mark style='color:black'>- Sottotitolo</mark>\n\
        <mark style='color:black'>- Selezione estensione</mark>\n\
        <mark style='color:black'>- Selezione layer da rappresentare e loro ordine</mark>\n\
        <mark style='color:black'>- Impostazione dimensioni e orientamento carta</mark>\n\
        <mark style='color:black'>- Impostazione numero colonne, le righe vengono di conseguenza</mark>\n\
        <mark style='color:black'>- Impostazione scala, di default adatta</mark>\n\
        <mark style='color:black'>- Scelta percorso e tipo file di salvataggio (tutti i formati del salva come immagine)</i></mark>\n\
        <mark style='color:black'>- Il layout prodotto ha nome <mark style='color:red'><strong>'MultiMap_[<i>orientamento</i>]_[<i>formato</i>]\n\
        <mark style='color:blue'><strong>NOTA BENE</strong></mark>\n\
        <mark style='color:black'><strong>Tutti i layer devon avere lo stesso SR</strong></mark>\n\
        <mark style='color:black'><strong>I layer che vogliamo in tutte le mappe devono essere visibili</strong></mark>\n\
        <mark style='color:black'><strong>Di default l'ordinamento è alfanumerico e gli elementi sul layout bloccati</strong></mark>\n\
        <mark style='color:black'><strong>Modificare l'ordinamento in stampa agendo nella casella di selezione layer\n\
        <mark style='color:red'><i><strong>Qualora l'adattamento non dia quanto voluto agire sulla scala\n\
		")
        
    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
        
    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        
        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).

        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_TIT,
                self.tr('Composition Title'),
                optional = True,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterExpression(
                self.INPUT_EXP,
                self.tr('Map Subtitle'),
                #defaultValue= " ",
                optional = True,
            )
        )
        
        self.addParameter(
            QgsProcessingParameterExtent(
                self.INPUT_EXT,
                self.tr('Extension'),
                optional = False,
                #[0,0,0,0]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LYR,
                self.tr('Layer sequence'),
                layerType = QgsProcessing.TypeMapLayer,
                defaultValue = None
            )
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.PAPER_DIM,
                self.tr('Paper format'),
                ['A0','A1','A2','A3','A4','A5'],
                defaultValue = 3
            )
        )
    
        self.addParameter(
            QgsProcessingParameterEnum(
                self.PAPER_ORI,
                self.tr('Landscape / Portrait'),
                ['Landscape','Portrait'],
                defaultValue = 0
            )
        )
    
        self.addParameter(
                QgsProcessingParameterNumber(
                    self.COLON_NUM,
                    self.tr('Column number'),
                    defaultValue = 1
                )
            )
            
        self.addParameter(
                QgsProcessingParameterString(
                    self.INPUT_SCL,
                    self.tr('Scale 1:'),
                    defaultValue = 'Fit'
                )
            )
    
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_PDF,
                self.tr('Select file type and destination'),
                fileFilter = 'File format (*.bmp *.jpg *.jpeg *.pdf *.png *.svg *.tiff)',
                #defaultValue = 'C:\\Users\\Delta\\Desktop\\SCRIPT GIS\\MultiMap\\TestMultiMap.jpg',
                optional = True,
                createByDefault = False
                )
            )
    
    def processAlgorithm(self, parameters, context, feedback):
        
        titolo = self.parameterAsString(
            parameters,
            self.INPUT_TIT,
            context)
        estensione = self.parameterAsExtent(
            parameters,
            self.INPUT_EXT,
            context)
            
        espressione = self.parameterAsString(
            parameters,
            self.INPUT_EXP,
            context)
        estensione_crs = self.parameterAsExtentCrs(
            parameters,
            self.INPUT_EXT,
            context)
            
        draw_lyr = self.parameterAsMatrix(
            parameters,
            self.INPUT_LYR,
            context)
        
        paper_dim = self.parameterAsString(
            parameters,
            self.PAPER_DIM,
            context)
            
        paper_ori = self.parameterAsString(
            parameters,
            self.PAPER_ORI,
            context)
        
        map_scala = self.parameterAsString(
            parameters,
            self.INPUT_SCL,
            context)
        
        col_num = self.parameterAsInt(
            parameters,
            self.COLON_NUM,
            context)
        
        file_dest = self.parameterAsString(
            parameters,
            self.OUTPUT_PDF,
            context)
        
        """
        Here is where the processing itself takes place.
        """
        
        #Inizialize references
        project = QgsProject.instance()             #gets a reference to the project instance
        manager = project.layoutManager()           #gets a reference to the layout manager
        root = project.layerTreeRoot()              #get reference to tree root
        
        def get_group_layers(group):
        #   print('- group: ' + group.name())
            for child in group.children():
                if isinstance(child, QgsLayerTreeGroup):
                    # Recursive call to get nested groups
                    get_group_layers(child)
                else:
                    if child.isVisible() or child.name() == map.id():
                        layer_set.append(QgsProject.instance().mapLayersByName(child.name())[0])
                        #print(child.name())
        
        #Imposta il nome, numero di colonne e righe e dimensioni in mm
        #prefisso campo da cui tematizzare e scala di rappresemtazione

        pagesize = 'A'+ paper_dim                                  #0. formato pagina
        bordo = 20                                                 #1. bordo foglio in mm
        if paper_ori == '0':
            layoutName = "MultiMap_Landscape_" + pagesize          #2. nome layout Landscape)
        else:
            layoutName = "MultiMap_Portrait_" + pagesize           #2. nome layout Portrait)

        if  'Fit' not in map_scala:
            map_scala = float(map_scala)         #4. scala di stampa

        #colleziona i nomi dei layer variabili da inserire
        layer_names = []
        for layer in draw_lyr:
            layer_names.append(layer[:len(layer)-37])
        #print('variable ', layer_names)

        # Compute the number of steps to display within the progress bar
        total = 100.0 / len(layer_names) if len(layer_names) else 0

        #Rimuove il layout se già presente
        layouts_list = manager.printLayouts()
        for layout in layouts_list:
            if layout.name() == layoutName:
                manager.removeLayout(layout)

        # e lo ricrea
        layout = QgsPrintLayout(project)
        layout.initializeDefaults()
        layout.setName(layoutName)
        #feedback.pushInfo(paper_ori)
        if paper_ori == '0':
            layout.pageCollection().page(0).setPageSize(pagesize, QgsLayoutItemPage.Orientation.Landscape)
        else:
            layout.pageCollection().page(0).setPageSize(pagesize, QgsLayoutItemPage.Orientation.Portrait)
        manager.addLayout(layout)

        #calcola dimensione mappa in funzione del foglio meno i bordi in mm
        xm = (layout.pageCollection().page(0).pageSize().width()-2*bordo)/col_num
        ym = (layout.pageCollection().page(0).pageSize().height()-2*bordo)/math.ceil(len(layer_names)/col_num)

        #Imposta il contatore di mappe a zero e fit mappa
        canvas = iface.mapCanvas()
        #print(estensione.height())
        if estensione.height() == 0 and estensione.width() == 0:
            canvas.setExtent(iface.activeLayer().extent())
        else:
            canvas.setExtent(estensione)
        canvas.refresh()
        count = 0

        for r in range (math.ceil(len(layer_names)/col_num)):
            if len(layer_names) - r*col_num > col_num:
                ncol = col_num
            else:
                ncol = len(layer_names) - r*col_num
            
            #print('ncol ', ncol)
            
            for c in range (ncol):
            
                #Aggiunge una mappa nel layout e la mette in posizione
                map = QgsLayoutItemMap(layout)
                map.setRect(20, 20, 20, 20)
                #map.setExtent(canvas.extent())
                map.setExtent(estensione)
                map.setId(layer_names[count])
                #print(map.id())
                map.attemptMove(QgsLayoutPoint(bordo+xm*c, bordo+ym*r, QgsUnitTypes.LayoutMillimeters))
                map.attemptResize(QgsLayoutSize(xm, ym, QgsUnitTypes.LayoutMillimeters))
                
                #centra la mappa definitiva e la mette in scala
                extent = map.extent()
                
                #override scale and fit map
                if map_scala == 'Fit':
                    h_map_scala = int(math.ceil(estensione.height()/map.rect().height()/10)*10000)
                    w_map_scala = int(math.ceil(estensione.width() /map.rect().width()/10)*10000)
                    
                    map_scala = max(h_map_scala,w_map_scala)
                 
                #print(map.scale() , map_scala)
              
                center = extent.center()
                newwidth  = extent.width()  / map.scale() * map_scala
                newheight = extent.height() / map.scale() * map_scala
                x1 = center.x() - 0.5 * newwidth
                y1 = center.y() - 0.5 * newheight
                x2 = center.x() + 0.5 * newwidth
                y2 = center.y() + 0.5 * newheight
                map.setExtent(QgsRectangle(x1, y1, x2, y2))
                
                #aggiunge la mappa al layout di stampa
                layout.addLayoutItem(map)
                
                layer_set = []
                for child in root.children():
                    if isinstance(child, QgsLayerTreeGroup):
                        get_group_layers(child)
                    elif isinstance(child, QgsLayerTreeLayer):
                        #print('child ', child.name(), 'mapid ' , map.id())
                        correct = child.name().replace(' ','_')
                        #print(child.name(), correct)
                        if child.isVisible() or correct == map.id():
                                #print('child ', child.name(), 'mapid ' , map.id())
                                layer_set.append(QgsProject.instance().mapLayersByName(child.name())[0])
                                #print('inserito ', child.name())
                #print('mapid ', map.id())
                #print('layer_set ',layer_set)
                
                #seleziona e blocca il set di layer sulla mappa
                map.setLayers(layer_set)
                map.setKeepLayerSet(True)
                map.setKeepLayerStyles(True)
                map.setBackgroundEnabled(False)
                map.setFrameEnabled(True)
                map.setFrameStrokeColor(QColor.fromRgb(255,255,255))
                map.setFrameStrokeWidth(QgsLayoutMeasurement(1,QgsUnitTypes.LayoutMillimeters))
                map.setLocked(True)
                
                #Aggiunge il titolo alla mappa
                title = QgsLayoutItemLabel(layout)
                title.setText(map.id())
                title.setFont(QFont("Arial Black", 12))
                title.adjustSizeToText()
                title.attemptMove(QgsLayoutPoint(bordo+xm*c, bordo+ym*r, QgsUnitTypes.LayoutMillimeters))
                layout.addLayoutItem(title)
                title.setLocked(True)
                
                #Aggiunge il sottitolo alla mappa
                title = QgsLayoutItemLabel(layout)
                if "layer:='" in espressione:
                    a = (espressione.partition("'")[0])
                    b = espressione.partition("'")[2].partition("'")[2]
                    espressione = a + "'" + map.id() + "'" + b
                    #feedback.pushInfo(espressione)
                    title.setText('[%' + espressione + '%]')
                else:
                    title.setText(espressione)																																					
																										
                title.setFont(QFont("Arial", 10))
                title.adjustSizeToText()
                title.attemptMove(QgsLayoutPoint(bordo+xm*c, bordo+5+ym*r, QgsUnitTypes.LayoutMillimeters))
                layout.addLayoutItem(title)
                title.setLocked(True)
                
                #Aggiunge una barra di scala
                scalebar = QgsLayoutItemScaleBar(layout)
                scalebar.setStyle('Numeric')
                #scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
                #scalebar.setNumberOfSegments(4)
                #scalebar.setNumberOfSegmentsLeft(0)
                #scalebar.setUnitsPerSegment(0.5)
                scalebar.setLinkedMap(map)
                #scalebar.setUnitLabel('km')
                scalebar.setFont(QFont('Arial', 8))
                scalebar.update()
                layout.addLayoutItem(scalebar)
                scalebar.attemptMove(QgsLayoutPoint(bordo+xm*c, bordo+8+ym*r, QgsUnitTypes.LayoutMillimeters))
                scalebar.setLocked(True)

                # Update the progress bar
                feedback.setProgress(int(count * total))

                #passa alla mappa successiva
                count += 1
                
        label = QgsLayoutItemLabel(layout)
        label.setText(titolo)
        label.setFont(QFont('Arial Black', 18))
        label.adjustSizeToText()
        layout.addLayoutItem(label)
        label.attemptMove(QgsLayoutPoint(bordo, bordo-10, QgsUnitTypes.LayoutMillimeters)) 
        label.setLocked(True)
        exporter = QgsLayoutExporter (layout)
        if '.pdf' in file_dest:
            exporter.exportToPdf (file_dest, QgsLayoutExporter.PdfExportSettings())
        else:
            exporter.exportToImage (file_dest, QgsLayoutExporter.ImageExportSettings ())
        
        feedback.pushInfo("WOW The plugin is working as it should, created: " + layoutName + '\n')
        
        return {self.OUTPUT: None}

    #icona dell'algoritmo di processing
    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'icon.svg')))
        return icon
        
    def createInstance(self):
        return GeoLegendAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Multi Map Layout'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Multi Map Layout')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr()

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return MultiMapLayoutAlgorithm()