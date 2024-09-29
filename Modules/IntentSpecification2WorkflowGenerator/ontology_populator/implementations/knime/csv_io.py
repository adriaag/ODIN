from common import *
from ontology_populator.implementations.core import *
from ontology_populator.implementations.knime import KnimeImplementation, KnimeParameter, KnimeBaseBundle, KnimeDefaultFeature

csv_reader_implementation = KnimeImplementation(
    name='CSV Reader',
    algorithm=cb.DataLoading,
    parameters=[
        KnimeParameter("Reader File", XSD.string, '$$CSV_PATH$$', 'path', path='model/settings/file_selection/path'),
        KnimeParameter("Reader Location flag", XSD.boolean, True, 'location_present',
                       path='model/settings/file_selection/path'),
        KnimeParameter("Reader Filesystem", XSD.string, None, 'file_system_type', path='model/settings/file_selection/path'),

        KnimeParameter("FSI SettingsModelID", XSD.string, 'SMID_ReaderFileChooser', 'SettingsModelID',
                       path='model/settings/file_selection_Internals'),
        KnimeParameter("FSI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path='model/settings/file_selection_Internals'),

        KnimeParameter("has_fs_port", XSD.boolean, False, 'has_fs_port',
                       path='model/settings/file_selection/file_system_chooser__Internals'),
        KnimeParameter("overwritten_by_variable", XSD.boolean, False, 'overwritten_by_variable',
                       path='model/settings/file_selection/file_system_chooser__Internals'),
        KnimeParameter("convenience_fs_category", XSD.string, 'LOCAL', 'convenience_fs_category',
                       path='model/settings/file_selection/file_system_chooser__Internals'),
        KnimeParameter("relative_to", XSD.string, 'knime.workflow', 'relative_to',
                       path='model/settings/file_selection/file_system_chooser__Internals'),
        KnimeParameter("mountpoint", XSD.string, 'LOCAL', 'mountpoint',
                       path='model/settings/file_selection/file_system_chooser__Internals'),
        KnimeParameter("spaceId", XSD.string, '', 'spaceId',
                       path='model/settings/file_selection/file_system_chooser__Internals'),
        KnimeParameter("spaceName", XSD.string, '', 'spaceName',
                       path='model/settings/file_selection/file_system_chooser__Internals'),
        KnimeParameter("custom_url_timeout", XSD.integer, 1000, 'custom_url_timeout',
                       path='model/settings/file_selection/file_system_chooser__Internals'),
        KnimeParameter("connected_fs", XSD.boolean, True, 'connected_fs',
                       path='model/settings/file_selection/file_system_chooser__Internals'),

        KnimeParameter("has_column_header", XSD.boolean, True, 'has_column_header', path='model/settings'),
        KnimeParameter("has_row_id", XSD.boolean, False, 'has_row_id', path='model/settings'),
        KnimeParameter("support_short_data_rows", XSD.boolean, False, 'support_short_data_rows',
                       path='model/settings'),
        KnimeParameter("skip_empty_data_rows", XSD.boolean, False, 'skip_empty_data_rows', path='model/settings'),
        KnimeParameter("prepend_file_idx_to_row_id", XSD.boolean, False, 'prepend_file_idx_to_row_id',
                       path='model/settings'),
        KnimeParameter("comment_char", XSD.string, '#', 'comment_char', path='model/settings'),
        KnimeParameter("column_delimiter", XSD.string, ',', 'column_delimiter', path='model/settings'),
        KnimeParameter("quote_char", XSD.string, '"', 'quote_char', path='model/settings'),
        KnimeParameter("quote_escape_char", XSD.string, '"', 'quote_escape_char', path='model/settings'),
        KnimeParameter("use_line_break_row_delimiter", XSD.boolean, True, 'use_line_break_row_delimiter',
                       path='model/settings'),
        KnimeParameter("row_delimiter", XSD.string, '%%00013%%00010', 'row_delimiter', path='model/settings'),
        KnimeParameter("autodetect_buffer_size", XSD.integer, 1048576, 'autodetect_buffer_size',
                       path='model/settings'),

        KnimeParameter("spec_merge_mode_Internals", XSD.string, 'UNION', 'spec_merge_mode_Internals',
                       path='model/advanced_settings'),
        KnimeParameter("fail_on_differing_specs", XSD.boolean, True, 'fail_on_differing_specs',
                       path='model/advanced_settings'),
        KnimeParameter("append_path_column_Internals", XSD.boolean, False, 'append_path_column_Internals',
                       path='model/advanced_settings'),
        KnimeParameter("path_column_name_Internals", XSD.string, 'Path', 'path_column_name_Internals',
                       path='model/advanced_settings'),
        KnimeParameter("limit_data_rows_scanned", XSD.boolean, True, 'limit_data_rows_scanned',
                       path='model/advanced_settings'),
        KnimeParameter("max_data_rows_scanned", XSD.long, 10000, 'max_data_rows_scanned',
                       path='model/advanced_settings'),
        KnimeParameter("save_table_spec_config_Internals", XSD.boolean, True, 'save_table_spec_config_Internals',
                       path='model/advanced_settings'),
        KnimeParameter("limit_memory_per_column", XSD.boolean, True, 'limit_memory_per_column',
                       path='model/advanced_settings'),
        KnimeParameter("maximum_number_of_columns", XSD.integer, 8192, 'maximum_number_of_columns',
                       path='model/advanced_settings'),
        KnimeParameter("quote_option", XSD.string, 'REMOVE_QUOTES_AND_TRIM', 'quote_option',
                       path='model/advanced_settings'),
        KnimeParameter("replace_empty_quotes_with_missing", XSD.boolean, True, 'replace_empty_quotes_with_missing',
                       path='model/advanced_settings'),
        KnimeParameter("thousands_separator", XSD.string, '%%00000', 'thousands_separator',
                       path='model/advanced_settings'),
        KnimeParameter("decimal_separator", XSD.string, '.', 'decimal_separator', path='model/advanced_settings'),

        KnimeParameter("skip_lines", XSD.boolean, False, 'skip_lines', path='model/limit_rows'),
        KnimeParameter("number_of_lines_to_skip", XSD.long, 1, 'number_of_lines_to_skip', path='model/limit_rows'),
        KnimeParameter("skip_data_rows", XSD.boolean, False, 'skip_data_rows', path='model/limit_rows'),
        KnimeParameter("number_of_rows_to_skip", XSD.long, 1, 'number_of_rows_to_skip', path='model/limit_rows'),
        KnimeParameter("limit_data_rows", XSD.boolean, False, 'limit_data_rows', path='model/limit_rows'),
        KnimeParameter("max_rows", XSD.long, 50, 'max_rows', path='model/limit_rows'),

        KnimeParameter("charset", XSD.string, None, 'charset', path='model/encoding'),

        KnimeParameter("FMI SettingsModelID", XSD.string, 'SMID_FilterMode', 'SettingsModelID',
                       path='model/settings/file_selection/filter_mode_Internals'),
        KnimeParameter("FMI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path='model/settings/file_selection/filter_mode_Internals'),

        KnimeParameter("filter_mode", XSD.string, 'FILE', 'filter_mode',
                       path='model/settings/file_selection/filter_mode'),
        KnimeParameter("include_subfolders", XSD.boolean, False, 'include_subfolders',
                       path='model/settings/file_selection/filter_mode'),

        KnimeParameter("filter_files_extension", XSD.boolean, False, 'filter_files_extension',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("files_extension_expression", XSD.string, '', 'files_extension_expression',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("files_extension_case_sensitive", XSD.boolean, False, 'files_extension_case_sensitive',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("filter_files_name", XSD.boolean, False, 'filter_files_name',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("files_name_expression", XSD.string, '*', 'files_name_expression',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("files_name_case_sensitive", XSD.boolean, False, 'files_name_case_sensitive',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("files_name_filter_type", XSD.string, 'WILDCARD', 'files_name_filter_type',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("include_hidden_files", XSD.boolean, False, 'include_hidden_files',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("include_special_files", XSD.boolean, True, 'include_special_files',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("filter_folders_name", XSD.boolean, False, 'filter_folders_name',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("folders_name_expression", XSD.string, '*', 'folders_name_expression',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("folders_name_case_sensitive", XSD.boolean, False, 'folders_name_case_sensitive',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("folders_name_filter_type", XSD.string, 'WILDCARD', 'folders_name_filter_type',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("include_hidden_folders", XSD.boolean, False, 'include_hidden_folders',
                       path='model/settings/file_selection/filter_mode/filter_options'),
        KnimeParameter("follow_links", XSD.boolean, True, 'follow_links',
                       path='model/settings/file_selection/filter_mode/filter_options'),
    ],
    input=[],
    output=[
        cb.TabularDataset,
    ],
    knime_node_factory = 'org.knime.base.node.io.filehandling.csv.reader.CSVTableReaderNodeFactory',
    knime_bundle = KnimeBaseBundle,
    knime_feature = KnimeDefaultFeature
)

csv_reader_local_component = Component(
    name='CSV Local reader',
    implementation=csv_reader_implementation,
    transformations=[
        LoaderTransformation(),
    ],
    overriden_parameters=[
        # ParameterSpecification(list(csv_reader_implementation.parameters.keys())[1], True),
        # ParameterSpecification(list(csv_reader_implementation.parameters.keys())[2], 'LOCAL'),
        ParameterSpecification([param for param in csv_reader_implementation.parameters.keys() if param.knime_key == 'location_present'][0], True),
        ParameterSpecification([param for param in csv_reader_implementation.parameters.keys() if param.knime_key == 'file_system_type'][0], 'LOCAL')
    ],
    exposed_parameters=[
        list(csv_reader_implementation.parameters.keys())[0]
    ],
)

csv_writer_implementation = KnimeImplementation(
    name='CSV Writer',
    algorithm=cb.DataStoring,
    parameters=[
        KnimeParameter('Writer File', XSD.string, r"/home/zyad/Desktop/output.csv", 'path',
                       path='model/settings/file_chooser_settings/path'),
        KnimeParameter('Writer Location flag', XSD.boolean, True, 'location_present',
                       path='model/settings/file_chooser_settings/path'),
        KnimeParameter('Writer Filesystem', XSD.string, None, 'file_system_type',
                       path='model/settings/file_chooser_settings/path'),

        KnimeParameter('Create Missing Folders', XSD.boolean, True, 'create_missing_folders',
                       path='model/settings/file_chooser_settings'),
        KnimeParameter('On Existing File', XSD.string, 'fail', 'if_path_exists',
                       path='model/settings/file_chooser_settings'),

        KnimeParameter("FCSI SettingsModelID", XSD.string, 'SMID_WriterFileChooser', 'SettingsModelID',
                       path='model/settings/file_chooser_settings_Internals'),
        KnimeParameter("FCSI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path='model/settings/file_chooser_settings_Internals'),

        KnimeParameter("has_fs_port", XSD.boolean, False, 'has_fs_port',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),
        KnimeParameter("overwritten_by_variable", XSD.boolean, False, 'overwritten_by_variable',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),
        KnimeParameter("convenience_fs_category", XSD.string, 'LOCAL', 'convenience_fs_category',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),
        KnimeParameter("relative_to", XSD.string, 'knime.workflow.data', 'relative_to',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),
        KnimeParameter("mountpoint", XSD.string, 'LOCAL', 'mountpoint',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),
        KnimeParameter("spaceId", XSD.string, '', 'spaceId',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),
        KnimeParameter("spaceName", XSD.string, '', 'spaceName',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),
        KnimeParameter("custom_url_timeout", XSD.integer, 1000, 'custom_url_timeout',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),
        KnimeParameter("connected_fs", XSD.boolean, True, 'connected_fs',
                       path='model/settings/file_chooser_settings/file_system_chooser__Internals'),

        KnimeParameter("FMI SettingsModelID", XSD.string, 'SMID_FilterMode', 'SettingsModelID',
                       path='model/settings/file_chooser_settings/filter_mode_Internals'),
        KnimeParameter("FMI EnabledStatus", XSD.boolean, True, 'EnabledStatus',
                       path='model/settings/file_chooser_settings/filter_mode_Internals'),

        KnimeParameter('Column Delimieter', XSD.string, ',', 'column_delimiter',
                       path='model/settings'),
        KnimeParameter('Row Delimieter', XSD.string, None, 'row_delimiter',
                       path='model/settings'),
        KnimeParameter('Quote char', cb.term('char'), '"', 'quote_char',
                       path='model/settings'),
        KnimeParameter('Quote escape char', cb.term('char'), '"', 'quote_escape_char',
                       path='model/settings'),
        KnimeParameter('Write column header', XSD.boolean, True, 'write_column_header',
                       path='model/settings'),
        KnimeParameter('Skip column header on append', XSD.boolean, False, 'skip_column_header_on_append',
                       path='model/settings'),
        KnimeParameter('Write row header', XSD.boolean, False, 'write_row_header',
                       path='model/settings'),

        KnimeParameter('missing_value_pattern', XSD.string, '', 'missing_value_pattern',
                       path='model/advanced_settings'),
        KnimeParameter('compress_with_gzip', XSD.boolean, False, 'compress_with_gzip',
                       path='model/advanced_settings'),
        KnimeParameter('quote_mode', XSD.string, "STRINGS_ONLY", 'quote_mode',
                       path='model/advanced_settings'),
        KnimeParameter('separator_replacement', XSD.string, '', 'separator_replacement',
                       path='model/advanced_settings'),
        KnimeParameter('decimal_separator', cb.term('char'), '.', 'decimal_separator',
                       path='model/advanced_settings'),
        KnimeParameter('use_scientific_format', XSD.boolean, False, 'use_scientific_format',
                       path='model/advanced_settings'),
        KnimeParameter('keep_trailing_zero_in_decimals', XSD.boolean, False, 'keep_trailing_zero_in_decimals',
                       path='model/advanced_settings'),

        KnimeParameter('comment_line_marker', XSD.string, '#', 'comment_line_marker',
                       path='model/comment_header_settings'),
        KnimeParameter('comment_indentation', XSD.string, '%%00009', 'comment_indentation',
                       path='model/comment_header_settings'),
        KnimeParameter('add_time_to_comment', XSD.boolean, False, 'add_time_to_comment',
                       path='model/comment_header_settings'),
        KnimeParameter('add_user_to_comment', XSD.boolean, False, 'add_user_to_comment',
                       path='model/comment_header_settings'),
        KnimeParameter('add_table_name_to_comment', XSD.boolean, False, 'add_table_name_to_comment',
                       path='model/comment_header_settings'),
        KnimeParameter('add_custom_text_to_comment', XSD.boolean, False, 'add_custom_text_to_comment',
                       path='model/comment_header_settings'),
        KnimeParameter('custom_comment_text', XSD.string, '', 'custom_comment_text',
                       path='model/comment_header_settings'),

        KnimeParameter('character_set', XSD.string, 'windows-1252', 'character_set',
                       path='model/encoding'),
    ],
    input=[cb.TabularDataset],
    output=[],
    knime_node_factory = 'org.knime.base.node.io.filehandling.csv.writer.CSVWriter2NodeFactory',
    knime_bundle = KnimeBaseBundle,
    knime_feature = KnimeDefaultFeature
)

csv_writer_local_component = Component(
    name='CSV Local writer',
    implementation=csv_writer_implementation,
    transformations=[],
    overriden_parameters=[
        # ParameterSpecification(list(csv_writer_implementation.parameters.keys())[1], True),
        # ParameterSpecification(list(csv_writer_implementation.parameters.keys())[2], 'LOCAL'),
        ParameterSpecification([param for param in csv_writer_implementation.parameters.keys() if param.knime_key == 'location_present'][0], True),
        ParameterSpecification([param for param in csv_writer_implementation.parameters.keys() if param.knime_key == 'file_system_type'][0], 'LOCAL')
    ],
    exposed_parameters=[
        list(csv_writer_implementation.parameters.keys())[0],
        list(csv_writer_implementation.parameters.keys())[3],
        list(csv_writer_implementation.parameters.keys())[4],
        list(csv_writer_implementation.parameters.keys())[18],
        list(csv_writer_implementation.parameters.keys())[19],
        list(csv_writer_implementation.parameters.keys())[20],
        list(csv_writer_implementation.parameters.keys())[21],
        list(csv_writer_implementation.parameters.keys())[22],
        list(csv_writer_implementation.parameters.keys())[23],
        list(csv_writer_implementation.parameters.keys())[24],
    ]

)
