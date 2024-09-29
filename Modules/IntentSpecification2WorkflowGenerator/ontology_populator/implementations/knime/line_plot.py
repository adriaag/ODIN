from common import *
from ..core import *
from .knime_implementation import KnimeImplementation, KnimeParameter, KnimeJSBundle, KnimeJSViewsFeature

lineplot_visualizer_implementation = KnimeImplementation(

    name = "Line Plot Visualizer",
    algorithm = cb.LinePlot,
    parameters = [

        KnimeParameter("generateImage", XSD.boolean, True, 'generateImage', path="model"),
        KnimeParameter("Maximum Number of Rows", XSD.int, 2500, 'maxRows', path="model"),
        KnimeParameter("Selection Column Name", XSD.string, "Selected (Line Plot)", 'selectionColumnName', path="model"),
        KnimeParameter("Auto Range Axes", XSD.boolean, True, 'autoRange', path="model"),
        KnimeParameter("X Axis Label", XSD.string, "", 'xAxisLabel', path="model"), ### Optional
        KnimeParameter("Y Axis Label", XSD.string, "", 'yAxisLabel', path="model"), ### Optional
        KnimeParameter("X Axis Min", XSD.string, None, 'xAxisMin', path="model"),
        KnimeParameter("X Axis Max", XSD.string, None, 'xAxisMax', path="model"),
        KnimeParameter("Y Axis Min", XSD.string, None, 'yAxisMin', path="model"),
        KnimeParameter("Y Axis Max", XSD.string, None, 'yAxisMax', path="model"),
        KnimeParameter("Dot Size", XSD.string, "3", 'dot_size', path="model"),
        KnimeParameter("Image Width", XSD.int, 800, 'imageWidth', path="model"),
        KnimeParameter("Image Height", XSD.int, 600, 'imageHeight', path="model"),
        KnimeParameter("Background Color", XSD.string, "rgba(255,255,255,1.0)", 'backgroundColor', path="model"),
        KnimeParameter("Data Area Color", XSD.string, "rgba(255,255,255,1.0)", 'dataAreaColor', path="model"),
        KnimeParameter("Grid Color", XSD.string, "rgba(230,230,230,1.0)", 'gridColor', path="model"),
        KnimeParameter("Display Full Screen Button", XSD.boolean, True, 'displayFullscreenButton', path="model"),
        KnimeParameter("Missing Value Method", XSD.string, "noGap", 'missingValueMethod', path="model"), ### Very Important ["noGap", "Gap", "removeColumn"]
        KnimeParameter("Show Warning In View", XSD.boolean, True, 'showWarningInView', path="model"),
        KnimeParameter("X Axis Column", XSD.string, "$$ANY_COLUMN$$", 'xCol', condition="$$X_COL$$", path="model"), ### Very Important
        KnimeParameter("Y Columns Filter Type", XSD.string, "STANDARD", 'filter-type', path="model/yCols"),
        KnimeParameter("Y Columns Included Names Array Size", RDF.List, "$$ANY_COLUMN$$", 'included_names',
                       condition = "$$INCLUDED$$", path="model/yCols"), ### Very Important
        ### Creation of Parameters: KnimeParameter("Included Y Axis Column", XSD.string, "$$COLUMN_NAME$$", '$$COLUMN_ORDER$$', path="model/yCols/included_names")
        KnimeParameter("Y Columns Excluded Names Array Size", RDF.List, "$$ANY_COLUMN$$", 'excluded_names',
                       condition = "$$EXCLUDED$$", path="model/yCols"), ### Very Important
        ### Creation of Parameters: KnimeParameter("Excluded Y Axis Column", XSD.string, "$$COLUMN_NAME$$", '$$COLUMN_ORDER$$', path="model/yCols/excluded_names")
        KnimeParameter("Enforce option", XSD.string, "EnforceExclusion", 'enforce_option', path="model/yCols"),
        KnimeParameter("NP Pattern", XSD.string, "", 'pattern', path="model/yCols/name_pattern"), ### Very Important
        KnimeParameter("NP Type", XSD.string, "Wildcard", 'type', path="model/yCols/name_pattern"),
        KnimeParameter("NP Case Sensitive", XSD.boolean, True, 'caseSensitive', path="model/yCols/name_pattern"),
        KnimeParameter("NP Exclude Matching", XSD.boolean, False, 'excludeMatching', path="model/yCols/name_pattern"),
        KnimeParameter("Datatype Typelist String Value", XSD.boolean, False, 'org.knime.core.data.StringValue', path="model/yCols/datatype/typelist"),
        KnimeParameter("Datatype Typelist Int Value", XSD.boolean, False, 'org.knime.core.data.IntValue', path="model/yCols/datatype/typelist"),
        KnimeParameter("Datatype Typelist Boolean Value", XSD.boolean, False, 'org.knime.core.data.BooleanValue', path="model/yCols/datatype/typelist"),
        KnimeParameter("Datatype Typelist Double Value", XSD.boolean, False, 'org.knime.core.data.DoubleValue', path="model/yCols/datatype/typelist"),
        KnimeParameter("Datatype Typelist Long Value", XSD.boolean, False, 'org.knime.core.data.LongValue', path="model/yCols/datatype/typelist"),
        KnimeParameter("Datatype Typelist Date and Time Value", XSD.boolean, False, 'org.knime.core.data.date.DateAndTimeValue', path="model/yCols/datatype/typelist"),
        KnimeParameter("Report On Missing Values", XSD.boolean, True, 'reportOnMissingValues', path="model"), ### Very Important,
        KnimeParameter("Use Domain Information", XSD.boolean, False, 'useDomainInformation', path="model"),
        KnimeParameter("Always Show Origin", XSD.boolean, False, 'enforceOrigin', path="model"),
        KnimeParameter("Enable Line Size Change", XSD.boolean, False, 'enableLineSizeChange', path="model"),
        KnimeParameter("Line Size", XSD.int, 2, 'line_size', path="model"),
        KnimeParameter("Chart Title", XSD.string, "", 'chartTitle', path="model"),
        KnimeParameter("Chart Subtitle", XSD.string, "", 'chartSubtitle', path="model"),
        KnimeParameter("Show Grid", XSD.boolean, True, 'showGrid', path="model"),
        KnimeParameter("Enable Mouse Crosshairs", XSD.boolean, False, 'showCrosshair', path="model"),
        KnimeParameter("Snap to Data Points", XSD.boolean, False, 'snapToPoints', path="model"),
        KnimeParameter("Enable Selection", XSD.boolean, True, 'enableSelection', path="model"),
        KnimeParameter("Enable Rectangular Selection", XSD.boolean, True, 'enableRectangleSelection', path="model"),
        KnimeParameter("Enable Lasso Selection", XSD.boolean, False, 'enableLassoSelection', path="model"),
        KnimeParameter("Resize to Full Window", XSD.boolean, True, 'resizeToWindow', path="model"),
        KnimeParameter("DTFI SettingsModelID", XSD.string, "SMID_datetime", 'SettingsModelID',
                       path="model/dateTimeFormats_Internals"),
        KnimeParameter("DTFI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/dateTimeFormats_Internals"),
        KnimeParameter("Global Date Time Locale", XSD.string, "en", 'globalDateTimeLocale', path="model/dateTimeFormats"),
        KnimeParameter("GDTLI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/dateTimeFormats/globalDateTimeLocale_Internals"),
        KnimeParameter("GDTLI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/dateTimeFormats/globalDateTimeLocale_Internals"),
        KnimeParameter("Global Date Format", XSD.string, "YYYY-MM-DD", 'globalDateFormat', path="model/dateTimeFormats"),
        KnimeParameter("GDFI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/dateTimeFormats/globalDateFormat_Internals"),
        KnimeParameter("GDFI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/dateTimeFormats/globalDateFormat_Internals"),
        KnimeParameter("Global Local Date Format", XSD.string, "YYYY-MM-DD", 'globalLocalDateFormat', path="model/dateTimeFormats"), ### Very Important
        KnimeParameter("GLDFI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/dateTimeFormats/globalLocalDateFormat_Internals"),
        KnimeParameter("GLDFI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/dateTimeFormats/globalLocalDateFormat_Internals"),
        KnimeParameter("Global Local Date and Time Format", XSD.string, "YYYY-MM-DD", 'globalLocalDateTimeFormat', path="model/dateTimeFormats"), ### Very Important
        KnimeParameter("GLDTI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/dateTimeFormats/globalLocalDateTimeFormat_Internals"),
        KnimeParameter("GLDTI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/dateTimeFormats/globalLocalDateTimeFormat_Internals"),
        KnimeParameter("Global Local Time Format", XSD.string, "HH:mm:ss", 'globalLocalTimeFormat', path="model/dateTimeFormats"), ### Very Important
        KnimeParameter("GLTFI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/dateTimeFormats/globalLocalTimeFormat_Internals"),
        KnimeParameter("GLTFI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/dateTimeFormats/globalLocalTimeFormat_Internals"),
        KnimeParameter("Global Zoned Date and Time Format", XSD.string, "YYYY-MM-DD z", 'globalZonedDateTimeFormat', path="model/dateTimeFormats"), ### Very Important
        KnimeParameter("GZDTI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/dateTimeFormats/globalZonedDateTimeFormat_Internals"),
        KnimeParameter("GZDTI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/dateTimeFormats/globalZonedDateTimeFormat_Internals"),
        KnimeParameter("Time Zone", XSD.string, "Europe/Madrid", 'timezone', path="model/dateTimeFormats"), ### Very Important
        KnimeParameter("TZI SettingsModelID", XSD.string, "SMID_string", 'SettingsModelID',
                       path="model/dateTimeFormats/timezone_Internals"),
        KnimeParameter("TZI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path="model/dateTimeFormats/timezone_Internals"),
        KnimeParameter("Enable View Configuration", XSD.boolean, True, 'enableViewConfiguration', path="model"),
        KnimeParameter("Enable Title Change", XSD.boolean, True, 'enableTitleChange', path="model"),
        KnimeParameter("Enable Subtitle Change", XSD.boolean, True, 'enableSubtitleChange', path="model"),
        KnimeParameter("Enable X Column Change", XSD.boolean, True, 'enableXColumnChange', path="model"),
        KnimeParameter("Enable Y Column Change", XSD.boolean, True, 'enableYColumnChange', path="model"),
        KnimeParameter("Enable X Axis Label Edit", XSD.boolean, True, 'enableXAxisLabelEdit', path="model"),
        KnimeParameter("Enable Y Axis Label Edit", XSD.boolean, True, 'enableYAxisLabelEdit', path="model"),
        KnimeParameter("Enable Dot Size Change", XSD.boolean, False, 'enableDotSizeChange', path="model"),
        KnimeParameter("Enable Panning", XSD.boolean, True, 'enablePanning', path="model"),
        KnimeParameter("Enable Zooming", XSD.boolean, True, 'enableZooming', path="model"),
        KnimeParameter("Enable Drag Zooming", XSD.boolean, False, 'enableDragZooming', path="model"),
        KnimeParameter("Show Zoom Reset Button", XSD.boolean, False, 'showZoomResetButton', path="model"),
        KnimeParameter("hideInWizard", XSD.boolean, False, 'hideInWizard', path="model"),
        KnimeParameter("showLegend", XSD.boolean, True, 'showLegend', path="model"),

    ],
    input = [
        [cb.NormalizedTabularDatasetShape, cb.TabularDataset]
    ],
    output = [
        cb.LinePlotVisualizationShape,
        cb.TabularDataset
    ],
    implementation_type = tb.VisualizerImplementation,
    knime_node_factory = 'org.knime.js.base.node.viz.plotter.line.LinePlotNodeFactory',
    knime_bundle = KnimeJSBundle, 
    knime_feature = KnimeJSViewsFeature

)

lineplot_params = list(lineplot_visualizer_implementation.parameters.keys())

exposed_params = [
    'xCol', ### x-axis column
    # Creating yCols depending on the input, ### y-axis column
    'chartTitle', ### Title of the scatter plot
]

lineplot_visualizer_component = Component(
    name = "Line Plot Visualizer",
    implementation = lineplot_visualizer_implementation,
    exposed_parameters=[
        param for param in lineplot_visualizer_implementation.parameters.keys() if param.knime_key in exposed_params
    ],
    transformations = [
        CopyTransformation(1, 2)
    ]
)