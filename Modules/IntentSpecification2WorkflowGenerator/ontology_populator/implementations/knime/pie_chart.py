from common import *
from ontology_populator.implementations.core import *
from ontology_populator.implementations.knime.knime_implementation import KnimeImplementation, KnimeParameter, KnimeDynamicBundle, KnimeJSViewsFeature

piechart_visualizer_implementation = KnimeImplementation(
    name = "Pie_Donut Chart",
    algorithm = cb.PieChart,
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
        KnimeParameter("Pie Aggregation", XSD.string, "Sum", 'aggr', path="model"), ### Very Important [Occurrence Count, Sum, Average]
        KnimeParameter("AGGI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/aggr_Internals"),
        KnimeParameter("AGGI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/aggr_Internals"),
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
        KnimeParameter("frequency", XSD.string, "$$NUMERIC_COLUMN$$", 'freq', path="model"), ### Optional Very Important
        KnimeParameter("FrI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/freq_Internals"),
        KnimeParameter("FrI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/freq_Internals"),
        KnimeParameter("Process In Memory", XSD.boolean, True, 'processInMemory', path="model"),
        KnimeParameter("PIMI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/processInMemory_Internals"),
        KnimeParameter("PIMI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/processInMemory_Internals"),
        KnimeParameter("title", XSD.string, "Pie Chart", 'title', path="model"), ### Very Important
        KnimeParameter("TI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/title_Internals"),
        KnimeParameter("TI EnabledStatus", XSD.boolean, True, "EnabledStatus",
                      path="model/title_Internals"),
        KnimeParameter("subtitle", XSD.string, "", 'subtitle', path="model"), ### Very Important
        KnimeParameter("SUBI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/subtitle_Internals"),
        KnimeParameter("SUBI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/subtitle_Internals"),
        KnimeParameter("togglePie", XSD.boolean, False, 'togglePie', path="model"), ### Very Important [True-->Donut, False-->Pie]
        KnimeParameter("TPI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/togglePie_Internals"),
        KnimeParameter("TPI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/togglePie_Internals"),
        KnimeParameter("holeSize", XSD.double, 0.35, 'holeSize', path="model"),
        KnimeParameter("HSI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/holeSize_Internals"),
        KnimeParameter("HSI EnabledStatus", XSD.boolean, False, 'EnabledStatus',
                       path="model/holeSize_Internals"),
        KnimeParameter("insideTitle", XSD.string, "", 'insideTitle', path="model"),
        KnimeParameter("INI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/insideTitle_Internals"),
        KnimeParameter("INI EnabledStatus", XSD.boolean, False, 'EnabledStatus',
                       path="model/insideTitle_Internals"),
        KnimeParameter("customColors", XSD.boolean, False, 'customColors', path="model"), ### Optional Very Important
        KnimeParameter("CCI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/customColors_Internals"),
        KnimeParameter("CCI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/customColors_Internals"),
        KnimeParameter("legend", XSD.boolean, True, 'legend', path="model"), ### Very Important 
        KnimeParameter("LEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/legend_Internals"),
        KnimeParameter("LEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/legend_Internals"),
        KnimeParameter("showLabels", XSD.boolean, True, 'showLabels', path="model"), ### Very Important
        KnimeParameter("SLI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/showLabels_Internals"),
        KnimeParameter("SLI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/showLabels_Internals"),
        KnimeParameter("labelType", XSD.string, "Value", 'labelType', path="model"), ### Very Important
        KnimeParameter("LTI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/labelType_Internals"),
        KnimeParameter("LTI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/labelType_Internals"),
        KnimeParameter("labelThreshold", XSD.double, 0.05, 'labelThreshold', path="model"),
        KnimeParameter("LTHI SettingsModelID", XSD.string, "SMID_double", 'SettingsModelID',
                       path="model/labelThreshold_Internals"),
        KnimeParameter("LTHI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/labelThreshold_Internals"),
        KnimeParameter("Display Full Screen Button", XSD.boolean, True, 'displayFullscreenButton', path="model"),
        KnimeParameter("DFBI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/displayFullscreenButton_Internals"),
        KnimeParameter("DFBI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/displayFullscreenButton_Internals"),
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
        KnimeParameter("enableDonutToggle", XSD.boolean, True, 'enableDonutToggle', path="model"),
        KnimeParameter("EDTI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableDonutToggle_Internals"),
        KnimeParameter("EDTI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableDonutToggle_Internals"),
        KnimeParameter("enableHoleEdit", XSD.boolean, True, 'enableHoleEdit', path="model"),
        KnimeParameter("EHEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableHoleEdit_Internals"),
        KnimeParameter("EHEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableHoleEdit_Internals"),
        KnimeParameter("enableInsideTitleEdit", XSD.boolean, True, 'enableInsideTitleEdit', path="model"),
        KnimeParameter("EIEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableInsideTitleEdit_Internals"),
        KnimeParameter("EIEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableInsideTitleEdit_Internals"),
        KnimeParameter("enableColumnChooser", XSD.boolean, True, 'enableColumnChooser', path="model"),
        KnimeParameter("ECCI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableColumnChooser_Internals"),
        KnimeParameter("ECCI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableColumnChooser_Internals"),
        KnimeParameter("enableLabelEdit", XSD.boolean, True, 'enableLabelEdit', path="model"),
        KnimeParameter("ELEI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableLabelEdit_Internals"),
        KnimeParameter("ELEI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableLabelEdit_Internals"),
        KnimeParameter("enableSwitchMissValCat", XSD.boolean, True, 'enableSwitchMissValCat', path="model"),
        KnimeParameter("ESMI SettingsModelID", XSD.string, "SMID_boolean", 'SettingsModelID',
                       path="model/enableSwitchMissValCat_Internals"),
        KnimeParameter("ESMI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/enableSwitchMissValCat_Internals"),
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
        KnimeParameter("maxRows", XSD.integer, 2500, 'maxRows', path="model"),
        KnimeParameter("generateImage", XSD.boolean, True, 'generateImage', path="model"),
        KnimeParameter("customCSS", XSD.string, "", 'customCSS', path="model"),
        KnimeParameter("Node Dir", XSD.string, "org.knime.dynamic.js.base:nodes/:donutChart", 'nodeDir',
                       path="factory_settings"),

    ],
    input = [
        cb.TabularDataset
    ],
    output = [
        cb.PieChartVisualizationShape
    ],
    implementation_type = tb.VisualizerImplementation,
    knime_node_factory = 'org.knime.dynamic.js.v30.DynamicJSNodeFactory',
    knime_bundle = KnimeDynamicBundle,
    knime_feature = KnimeJSViewsFeature,
)

# piechart_expparams = [
#         list(piechart_visualizer_implementation.parameters.keys())[1], ### category column
#         list(piechart_visualizer_implementation.parameters.keys())[4], ### aggregation type: [Occurrence Count, Sum, Average]
#         list(piechart_visualizer_implementation.parameters.keys())[10], ### include missing value category: [True, False]
#         list(piechart_visualizer_implementation.parameters.keys())[13], ### frequency column (optional)
#         list(piechart_visualizer_implementation.parameters.keys())[19], ### pie chart visualization title
#         list(piechart_visualizer_implementation.parameters.keys())[22], ### pie chart visualization subtitle
#         list(piechart_visualizer_implementation.parameters.keys())[25], ### toggle Pie [True-->Donut, False-->Pie]
#         list(piechart_visualizer_implementation.parameters.keys())[34], ### having custom colors for the plot(optional)
#         list(piechart_visualizer_implementation.parameters.keys())[37], ### display legends for the visualization
#         list(piechart_visualizer_implementation.parameters.keys())[40], ### display labels for the visualization
#         list(piechart_visualizer_implementation.parameters.keys())[52], ### svg visualization width [default 600]
#         list(piechart_visualizer_implementation.parameters.keys())[53], ### svg visualization height [default 400]
# ]

# piechart_params = list(piechart_visualizer_implementation.parameters.keys())

exposed_params = [
    'cat', ### category column
    'includeMissValCat', ### include missing value category: [True, False]
    'freq', ### frequency column (optional)
    'title', ### pie chart visualization title
    'togglePie' ### toggle Pie [True-->Donut, False-->Pie]
]

piechart_sum_visualizer_component = Component(
    name = "Pie Chart Sum Visualizer",
    implementation = piechart_visualizer_implementation,
    exposed_parameters = [
        param for param in piechart_visualizer_implementation.parameters.keys() if param.knime_key in exposed_params
    ],
    overriden_parameters = [
        ParameterSpecification([param for param in piechart_visualizer_implementation.parameters.keys() if param.knime_key == 'aggr'][0], "Sum")
    ],
    transformations = []
)

piechart_count_visualizer_component = Component(
    name = "Pie Chart Count Visualizer",
    implementation = piechart_visualizer_implementation,
    exposed_parameters = [
        param for param in piechart_visualizer_implementation.parameters.keys() if param.knime_key in exposed_params and param.knime_key != 'freq'
    ],
    overriden_parameters = [
        ParameterSpecification([param for param in piechart_visualizer_implementation.parameters.keys() if param.knime_key == 'aggr'][0], "Occurence Count")
    ],
    transformations = []
)

piechart_avg_visualizer_component = Component(
    name = "Pie Chart Average Visualizer",
    implementation = piechart_visualizer_implementation,
    exposed_parameters = [
        param for param in piechart_visualizer_implementation.parameters.keys() if param.knime_key in exposed_params
    ],
    overriden_parameters = [
        ParameterSpecification([param for param in piechart_visualizer_implementation.parameters.keys() if param.knime_key == 'aggr'][0], "Average")
    ],
    transformations = []
)