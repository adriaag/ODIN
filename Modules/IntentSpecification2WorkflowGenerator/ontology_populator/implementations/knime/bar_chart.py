from common import *
from ontology_populator.implementations.core import *
from ontology_populator.implementations.knime import KnimeImplementation, KnimeParameter, KnimeDynamicBundle, KnimeJSViewsFeature

barchart_visualizer_implementation = KnimeImplementation(
    name = "Bar Chart Visualizer",
    algorithm = cb.BarChart,
    parameters = [

        KnimeParameter("Generate Image Model", XSD.boolean, False, 'generateImagemodel', path="model"),
        KnimeParameter("GIMI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/generateImagemodel_Internals"),
        KnimeParameter("GIMI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/generateImagemodel_Internals"),
        KnimeParameter("category", XSD.string, "$$CATEGORICAL$$", 'cat', path="model"), ### Very Important
        KnimeParameter("CI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/cat_Internals"),
        KnimeParameter("CI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/cat_Internals"),
        KnimeParameter("Sort Bars Alphabetically", XSD.boolean, False, 'sort', path="model"), ### Very Important
        KnimeParameter("SI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/sort_Internals"),
        KnimeParameter("SI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/sort_Internals"),
        KnimeParameter("Bar Aggregation", XSD.string, "Occurrence Count", 'aggr', path="model"), ### Very Important [Occurrence Count, Sum, Average]
        KnimeParameter("AGGI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/aggr_Internals"),
        KnimeParameter("AGGI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/aggr_Internals"),
        KnimeParameter("Filter Type", XSD.string, "STANDARD", 'filter-type', path="model/freq"), ### Optional Very Important
        KnimeParameter("Included Names Columns", RDF.List, "$$NUMERIC_COLUMNS$$", 'included_names',
                       condition = "$$INCLUDED$$", path="model/freq"), ### Very Important
        # KnimeParameter("Included Names 0", XSD.string, "$$NUMERICAL$$", '0', path="model/freq/included_names"), ### Very Important
        KnimeParameter("Excluded Names Columns", RDF.List, "$$NUMERIC_COLUMNS$$", 'excluded_names',
                       condition = "$$EXCLUDED$$", path="model/freq"), ### Very Important
        KnimeParameter("Enforce Option", XSD.string, "EnforceExclusion", 'enforce_option', path="model/freq"),
        KnimeParameter("NP Pattern", XSD.string, "", 'pattern', path="model/freq/name_pattern"), ### Need to Be Checked
        KnimeParameter("NP Type", XSD.string, "Wildcard", 'type', path="model/freq/name_pattern"),
        KnimeParameter("Np Case Sensitive", XSD.boolean, True, 'caseSensitive', path="model/freq/name_pattern"),
        KnimeParameter("NP Exclude Matching", XSD.boolean, False, 'excludeMatching', path="model/freq/name_pattern"),
        KnimeParameter("Datatype Typelist Integer Value", XSD.boolean, False, 'org.knime.core.data.IntValue',
                       path="model/freq/datatype/typelist"),
        KnimeParameter("Datatype Typelist Double Value", XSD.boolean, False, 'org.knime.core.data.DoubleValue',
                       path="model/freq/datatype/typelist"),  
        KnimeParameter("Process In Memory", XSD.boolean, True, 'processInMemory', path="model"),
        KnimeParameter("PIMI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/processInMemory_Internals"),
        KnimeParameter("PIMI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/processInMemory_Internals"),
        KnimeParameter("Report On Missing Values", XSD.boolean, True, 'reportOnMissingValues', path="model"), ### Very Important
        KnimeParameter("ROMVI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/reportOnMissingValues_Internals"),
        KnimeParameter("ROMVI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/reportOnMissingValues_Internals"), 
        KnimeParameter("Include Missing Values Category", XSD.boolean, True, 'includeMissValCat', path="model"), ### Very Important
        KnimeParameter("IMVCI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/includeMissValCat_Internals"),
        KnimeParameter("IMVCI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/includeMissValCat_Internals"),
        KnimeParameter("title", XSD.string, "Bar Chart", 'title', path="model"), ### Very Important
        KnimeParameter("TI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/title_Internals"),
        KnimeParameter("TI EnabledStatus", XSD.boolean, True, "EnabledStatus",
                      path="model/title_Internals"),
        KnimeParameter("subtitle", XSD.string, "", 'subtitle', path="model"), ### Very Important
        KnimeParameter("SUBI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/subtitle_Internals"),
        KnimeParameter("SUBI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/subtitle_Internals"),
        KnimeParameter("Category-axis Label", XSD.string, "", 'catLabel', path="model"), ### Very Important
        KnimeParameter("CALI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/catLabel_Internals"),
        KnimeParameter("CALI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/catLabel_Internals"),
        KnimeParameter("Frequency-axis Label", XSD.string, "", 'freqLabel', path="model"), ### Very Important
        KnimeParameter("FALI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/freqLabel_Internals"),
        KnimeParameter("FALI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/freqLabel_Internals"),
        KnimeParameter("Chart Type", XSD.string, "Grouped", 'chartType', path="model"), ### Very Important [Grouped, Stacked]
        KnimeParameter("CTI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/chartType_Internals"),
        KnimeParameter("CTI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/chartType_Internals"),
        KnimeParameter("Stagger Labels", XSD.boolean, False, 'staggerLabels', path="model"),
        KnimeParameter("SLI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/staggerLabels_Internals"),
        KnimeParameter("SLI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/staggerLabels_Internals"),
        KnimeParameter("Legend", XSD.boolean, True, 'legend', path="model"), ### Very Important 
        KnimeParameter("LEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/legend_Internals"),
        KnimeParameter("LEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/legend_Internals"),
        KnimeParameter("Tooltip", XSD.boolean, True, 'tooltip', path="model"),
        KnimeParameter("TTI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/tooltip_Internals"),
        KnimeParameter("TTI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/tooltip_Internals"),
        KnimeParameter("Bar Chart Orientation", XSD.boolean, False, 'orientation', path="model"), ### Very Important
        KnimeParameter("OI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/orientation_Internals"),
        KnimeParameter("OI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/orientation_Internals"),
        KnimeParameter("Display Full Screen Button", XSD.boolean, True, 'displayFullscreenButton', path="model"),
        KnimeParameter("DFBI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/displayFullscreenButton_Internals"),
        KnimeParameter("DFBI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/displayFullscreenButton_Internals"),
        KnimeParameter("Show Maximum Value", XSD.boolean, True, 'showMaximum', path="model"), ### Very Important
        KnimeParameter("SMI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/showMaximum_Internals"),
        KnimeParameter("SMI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/showMaximum_Internals"),
        KnimeParameter("Show Static Bar Values", XSD.boolean, False, 'showStaticBarValues', path="model"),
        KnimeParameter("SSBVI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/showStaticBarValues_Internals"),
        KnimeParameter("SSBVI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/showStaticBarValues_Internals"),
        KnimeParameter("svg_width", XSD.integer, 600, 'width', path="model/svg"), ### Very Important
        KnimeParameter("svg_height", XSD.integer, 400, 'height', path="model/svg"), ### Very Important
        KnimeParameter("svg_fullscreen", XSD.boolean, True, 'fullscreen', path="model/svg"), ### Very Important
        KnimeParameter("svg_showFullscreen", XSD.boolean, True, 'showFullscreen', path="model/svg"), ### Very Important
        KnimeParameter("SVGI SettingsModelID", XSD.string, "SMID_svg", 'SettingsModelID',
                       path="model/svg_Internals"),
        KnimeParameter("SVGI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/svg_Internals"),
        KnimeParameter("Show Warnings", XSD.boolean, True, 'showWarnings', path="model"),
        KnimeParameter("SWI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/showWarnings_Internals"),
        KnimeParameter("SWI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/showWarnings_Internals"),
        KnimeParameter("enableViewControls", XSD.boolean, True, 'enableViewControls', path="model"),
        KnimeParameter("EVCI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableViewControls_Internals"),
        KnimeParameter("EVCI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableViewControls_Internals"),
        KnimeParameter("enableStackedEdit", XSD.boolean, True, 'enableStackedEdit', path="model"),
        KnimeParameter("ESEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableStackedEdit_Internals"),
        KnimeParameter("ESEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableStackedEdit_Internals"),
        KnimeParameter("enableHorizontalToggle", XSD.boolean, True, 'enableHorizontalToggle', path="model"),
        KnimeParameter("EHTI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableHorizontalToggle_Internals"),
        KnimeParameter("EHTI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableHorizontalToggle_Internals"),
        KnimeParameter("enableStaggerToggle", XSD.boolean, True, 'enableStaggerToggle', path="model"),
        KnimeParameter("ESTI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableStaggerToggle_Internals"),
        KnimeParameter("ESTI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableStaggerToggle_Internals"),
        KnimeParameter("enableTitleEdit", XSD.boolean, True, 'enableTitleEdit', path="model"),
        KnimeParameter("ETEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableTitleEdit_Internals"),
        KnimeParameter("ETEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableTitleEdit_Internals"),
        KnimeParameter("enableSubtitleEdit", XSD.boolean, True, 'enableSubtitleEdit', path="model"),
        KnimeParameter("ESEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableSubtitleEdit_Internals"),
        KnimeParameter("ESEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableSubtitleEdit_Internals"),
        KnimeParameter("enableAxisEdit", XSD.boolean, True, 'enableAxisEdit', path="model"),
        KnimeParameter("EAEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableAxisEdit_Internals"),
        KnimeParameter("EAEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableAxisEdit_Internals"),
        KnimeParameter("enableSwitchMissValCat", XSD.boolean, True, 'enableSwitchMissValCat', path="model"),
        KnimeParameter("ESMI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableSwitchMissValCat_Internals"),
        KnimeParameter("ESMI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableSwitchMissValCat_Internals"),
        KnimeParameter("enableMaximumValue", XSD.boolean, True, 'enableMaximumValue', path="model"),
        KnimeParameter("EMVI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableMaximumValue_Internals"),
        KnimeParameter("EMVI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableMaximumValue_Internals"),
        KnimeParameter("enableStaticValuesEdit", XSD.boolean, True, 'enableStaticValuesEdit', path="model"),
        KnimeParameter("ESVEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableStaticValuesEdit_Internals"),
        KnimeParameter("ESVEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableStaticValuesEdit_Internals"),
        KnimeParameter("enableSelection", XSD.boolean, True, 'enableSelection', path="model"),
        KnimeParameter("ESI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableSelection_Internals"),
        KnimeParameter("ESI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableSelection_Internals"),
        KnimeParameter("subscribeToSelection", XSD.boolean, True, 'subscribeToSelection', path="model"),
        KnimeParameter("STSI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/subscribeToSelection_Internals"),
        KnimeParameter("STSI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/subscribeToSelection_Internals"),
        KnimeParameter("publishSelection", XSD.boolean, True, 'publishSelection', path="model"),
        KnimeParameter("PSI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/publishSelection_Internals"),
        KnimeParameter("PSI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/publishSelection_Internals"),
        KnimeParameter("displayClearSelectionButton", XSD.boolean, True, 'displayClearSelectionButton', path="model"),
        KnimeParameter("DCSI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/displayClearSelectionButton_Internals"),
        KnimeParameter("DCSI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/displayClearSelectionButton_Internals"),
        KnimeParameter("hideInWizard", XSD.boolean, False, 'hideInWizard', path="model"),
        KnimeParameter("maxRows", XSD.int, 2500, 'maxRows', path="model"),
        KnimeParameter("generateImage", XSD.boolean, True, 'generateImage', path="model"),
        KnimeParameter("customCSS", XSD.string, "", 'customCSS', path="model"),
        KnimeParameter("Node Dir", XSD.string, "org.knime.dynamic.js.base:nodes/:barChart", 'nodeDir',
                       path="factory_settings"),

    ],
    input = [
        cb.TabularDataset
    ],
    output = [
        cb.BarChartVisualizationShape
    ],
    implementation_type = tb.VisualizerImplementation,
    knime_node_factory = 'org.knime.dynamic.js.v30.DynamicJSNodeFactory',
    knime_bundle = KnimeDynamicBundle,
    knime_feature = KnimeJSViewsFeature,
)

# barchart_params = list(barchart_visualizer_implementation.parameters.keys())

exposed_params = [
    'cat', ### category column
    'sort', ### sort bars alphabetically
    'includeMissValCat', ### include missing value category: [True, False]
    'title', ### bar chart visualization title
    'chartType', ### chart type ['Grouped', 'Stacked']
    'orientation', ### bar chart orientaion
]

barchart_sum_visualizer_component = Component(
    name = "Bar Chart Sum Component",
    implementation = barchart_visualizer_implementation,
    exposed_parameters = [
        param for param in barchart_visualizer_implementation.parameters.keys() if param.knime_key in exposed_params
    ],
    overriden_parameters = [
        ParameterSpecification([param for param in barchart_visualizer_implementation.parameters.keys() if param.knime_key == 'aggr'][0], "Sum")
    ],
    transformations = []
)

barchart_count_visualizer_component = Component(
    name = "Bar Chart Count Component",
    implementation = barchart_visualizer_implementation,
    exposed_parameters = [
        param for param in barchart_visualizer_implementation.parameters.keys() if param.knime_key in exposed_params
    ],
    overriden_parameters = [
        ParameterSpecification([param for param in barchart_visualizer_implementation.parameters.keys() if param.knime_key == 'aggr'][0], "Occurence Count")
    ],
    transformations = []
)

barchart_avg_visualizer_component = Component(
    name = "Bar Chart Average Component",
    implementation = barchart_visualizer_implementation,
    exposed_parameters = [
        param for param in barchart_visualizer_implementation.parameters.keys() if param.knime_key in exposed_params
    ],
    overriden_parameters = [
        ParameterSpecification([param for param in barchart_visualizer_implementation.parameters.keys() if param.knime_key == 'aggr'][0], "Average")
    ],
    transformations = []
)