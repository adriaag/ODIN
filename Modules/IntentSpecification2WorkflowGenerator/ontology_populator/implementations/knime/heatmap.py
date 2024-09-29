from common import *
from ..core import *
from .knime_implementation import KnimeImplementation, KnimeParameter, KnimeJSBundle, KnimeJSViewsFeature

heatmap_visualizer_implementation = KnimeImplementation(

    name = "Heatmap Visualizer",
    algorithm = cb.HeatMap,
    parameters = [

        KnimeParameter("Custom CSS", XSD.string, "", 'customCSS', path="model"),
        KnimeParameter("hideInWizard", XSD.boolean, False, 'hideInWizard', path="model"),
        KnimeParameter("Show Warning In View", XSD.boolean, True, 'showWarningInView', path="model"),
        KnimeParameter("generateImage", XSD.boolean, True, 'generateImage', path="model"),
        KnimeParameter("Image Width", XSD.int, 800, 'imageWidth', path="model"),
        KnimeParameter("Image Height", XSD.int, 600, 'imageHeight', path="model"),
        KnimeParameter("Resize to Full Window", XSD.boolean, True, 'resizeToWindow', path="model"),
        KnimeParameter("Display Full Screen Button", XSD.boolean, True, 'displayFullscreenButton', path="model"),
        KnimeParameter("Chart Title", XSD.string, "", 'chartTitle', path="model"), ### Very Important
        KnimeParameter("Chart Subtitle", XSD.string, "", 'chartSubtitle', path="model"),
        KnimeParameter("Minimum Value", XSD.double, 0.0, 'minValue', path="model"), ### Very Important
        KnimeParameter("Maximum Value", XSD.double, 100.0, 'maxValue', path="model"), ### Very Important
        KnimeParameter("Use Custom Min", XSD.boolean, False, 'useCustomMin', path="model"), ### Very Important
        KnimeParameter("Use Custom Max", XSD.boolean, False, 'useCustomMax', path="model"), ### Very Important
        KnimeParameter("Enable View Configuration", XSD.boolean, True, 'enableViewConfiguration', path="model"),
        KnimeParameter("Enable Title Change", XSD.boolean, True, 'enableTitleChange', path="model"),
        KnimeParameter("Enable Color Mode Edit", XSD.boolean, True, 'enableColorModeEdit', path="model"),
        KnimeParameter("Enable Show Tool Tips", XSD.boolean, True, 'enableShowToolTips', path="model"),
        KnimeParameter("Show Tool Tips", XSD.boolean, False, 'showToolTips', path="model"),
        KnimeParameter("Three Color Gradient Array Size", XSD.int, 3, 'array-size', path="model/threeColorGradient"),
        KnimeParameter("Three Color Gradient Color 1", XSD.string, "#5E3C99", '0', path="model/threeColorGradient"),
        KnimeParameter("Three Color Gradient Color 2", XSD.string, "#F7F7F7", '1', path="model/threeColorGradient"),
        KnimeParameter("Three Color Gradient Color 3", XSD.string, "#E66101", '2', path="model/threeColorGradient"),
        KnimeParameter("Discrete Gradient Colors Array Size", XSD.int, 3, 'array-size', path="model/discreteGradientColors"),
        KnimeParameter("Discrete Gradient Colors Color 1", XSD.string, "#5E3C99", '0', path="model/discreteGradientColors"),
        KnimeParameter("Discrete Gradient Colors Color 2", XSD.string, "#F7F7F7", '1', path="model/discreteGradientColors"),
        KnimeParameter("Discrete Gradient Colors Color 3", XSD.string, "#E66101", '2', path="model/discreteGradientColors"),
        KnimeParameter("Continuous Gradient", XSD.boolean, True, 'continuousGradient', path="model"),
        KnimeParameter("Number of Discrete Colors", XSD.int, 3, 'numDiscreteColors', path="model"),
        KnimeParameter("Missing Value Color", XSD.string, "#000000", 'missingValueColor', path="model"),
        KnimeParameter("Upper Out of Range Color", XSD.string, "#000000", 'upperOutOfRangeColor', path="model"),
        KnimeParameter("Lower Out of Range Color", XSD.string, "#000000", 'lowerOutOfRangeColor', path="model"),
        KnimeParameter("Columns Filter Type", XSD.string, "STANDARD", 'filter-type', path="model/columns"),
        KnimeParameter("Colunms Included Names Array Size", RDF.List, "$$NUMERIC_COLUMNS$$", 'included_names',
                       condition="$$INCLUDED$$", path="model/columns"), ### TO BE CHECKED
        ### Creation of Parameters: KnimeParameter("Included Columns", XSD.string, "$$COLUMN_NAME$$", '$$COLUMN_ORDER$$', path="model/columns/included_names")
        KnimeParameter("Colunms Excluded Names Array Size", RDF.List, "$$NUMERIC_COLUMNS$$", 'excluded_names',
                       condition="$$EXCLUDED$$", path="model/columns"), ### TO BE CHECKED
        ### Creation of Parameters: KnimeParameter("Included Columns", XSD.string, "$$COLUMN_NAME$$", '$$COLUMN_ORDER$$', path="model/columns/excluded_names")
        KnimeParameter("Enforce option", XSD.string, "EnforceExclusion", 'enforce_option', path="model/columns"),
        KnimeParameter("NP Pattern", XSD.string, "", 'pattern', condition="$$ColumnName$$", path="model/columns/name_pattern"), ### Very Important
        KnimeParameter("NP Type", XSD.string, "Wildcard", 'type', path="model/columns/name_pattern"),
        KnimeParameter("NP Case Sensitive", XSD.boolean, True, 'caseSensitive', path="model/columns/name_pattern"),
        KnimeParameter("NP Exclude Matching", XSD.boolean, False, 'excludeMatching', path="model/columns/name_pattern"),
        KnimeParameter("Datatype Typelist String Value", XSD.boolean, False, 'org.knime.core.data.StringValue', path="model/columns/datatype/typelist"),
        KnimeParameter("Datatype Typelist Int Value", XSD.boolean, False, 'org.knime.core.data.IntValue', path="model/columns/datatype/typelist"),
        KnimeParameter("Datatype Typelist Boolean Value", XSD.boolean, False, 'org.knime.core.data.BooleanValue', path="model/columns/datatype/typelist"),
        KnimeParameter("Datatype Typelist Double Value", XSD.boolean, False, 'org.knime.core.data.DoubleValue', path="model/columns/datatype/typelist"),
        KnimeParameter("Datatype Typelist Long Value", XSD.boolean, False, 'org.knime.core.data.LongValue', path="model/columns/datatype/typelist"),
        KnimeParameter("Datatype Typelist Date and Time Value", XSD.boolean, False, 'org.knime.core.data.date.DateAndTimeValue', path="model/columns/datatype/typelist"),
        KnimeParameter("Label Column", XSD.string, "$$CATEGORICAL$$", 'labelColumn', path="model"), ### Very Important
        KnimeParameter("SVG Label Column", XSD.string, None, 'svgLabelColumn', path="model"),
        KnimeParameter("Subscribe Filter", XSD.boolean, True, 'subscribeFilter', path="model"),
        KnimeParameter("Enable Selection", XSD.boolean, True, 'enableSelection', path="model"),
        KnimeParameter("Publish Selection", XSD.boolean, True, 'publishSelection', path="model"),
        KnimeParameter("Subscribe Selection", XSD.boolean, True, 'subscribeSelection', path="model"),
        KnimeParameter("Selection Column Name", XSD.string, "Selected (Heatmap)", 'selectionColumnName', path="model"),
        KnimeParameter("Show Selected Rows Only", XSD.boolean, False, 'showSelectedRowsOnly', path="model"),
        KnimeParameter("Enable Show Selected Rows Only", XSD.boolean, True, 'enableShowSelectedRowsOnly', path="model"),
        KnimeParameter("Show Reset Selection Button", XSD.boolean, True, 'showResetSelectionButton', path="model"),
        KnimeParameter("Enable Paging", XSD.boolean, True, 'enablePaging', path="model"),
        KnimeParameter("Initial Page Size", XSD.int, 100, 'initialPageSize', path="model"),
        KnimeParameter("Enable Page Size Change", XSD.boolean, True, 'enablePageSizeChange', path="model"),
        KnimeParameter("Allowed Page Sizes Array Size", XSD.int, 4, 'array-size', path="model/allowedPageSizes"),
        KnimeParameter("Allowed Page Sizes 0", XSD.int, 100, '0', path="model/allowedPageSizes"),
        KnimeParameter("Allowed Page Sizes 1", XSD.int, 250, '1', path="model/allowedPageSizes"),
        KnimeParameter("Allowed Page Sizes 2", XSD.int, 500, '2', path="model/allowedPageSizes"),
        KnimeParameter("Allowed Page Sizes 3", XSD.int, 1000, '3', path="model/allowedPageSizes"),
        KnimeParameter("Enable Show All", XSD.boolean, False, 'enableShowAll', path="model"),
        KnimeParameter("Enable Zoom", XSD.boolean, True, 'enableZoom', path="model"),
        KnimeParameter("Enable Panning", XSD.boolean, True, 'enablePanning', path="model"),
        KnimeParameter("Show Zoom Reset Button", XSD.boolean, False, 'showZoomResetButton', path="model"),

    ],
    input = [
        [cb.NonNullTabularDatasetShape, cb.NormalizedTabularDatasetShape, cb.TabularDataset]
    ],
    output = [
        cb.HeatMapVisualizationShape,
        cb.TabularDataset
    ],
    implementation_type = tb.VisualizerImplementation,
    knime_node_factory = 'org.knime.js.base.node.viz.heatmap.HeatMapNodeFactory',
    knime_bundle = KnimeJSBundle,
    knime_feature = KnimeJSViewsFeature

)

heatmap_params = list(heatmap_visualizer_implementation.parameters.keys())

exposed_params = [
    'labelColumn', ### label column
    # Creating displayed cols depending on the input, ### numeric column
    'chartTitle', ### Title of the scatter plot
]

heatmap_visualizer_component = Component(
    name = "Heatmap Visualizer",
    implementation = heatmap_visualizer_implementation,
    exposed_parameters=[
        param for param in heatmap_visualizer_implementation.parameters.keys() if param.knime_key in exposed_params
    ],
    transformations = [
        CopyTransformation(1, 2),
        Transformation(
            query = '''
INSERT DATA {
    $output2 dmop:hasColumn _:heatmapColumn .
    _:heatmapColumn a dmop:Column ;
                    dmop:hasName "Selected (Heatmap)" ;
                    dmop:hasValue false .
}
'''
        )
    ]
)