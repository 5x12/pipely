from schema import Optional, Or, Regex, Schema, Use
from ppline.utils.const import dagmap_consts

def regex_safe(text: str):
    for symbol in ('.', '[', ']', '|', '^'):
        text = text.replace(symbol, f'\{symbol}')
    return rf'{text}'

def complete(regex):
    return rf'^{regex}\Z'

exec_path_separator = regex_safe(dagmap_consts.EXEC_PATH_SEPARATOR)

STAGE_NAMING_REGEX = r'[a-zA-Z_][-\w]*'
EXEC_REGEX = rf'\S*{exec_path_separator}[a-zA-Z_]\w*'

STEP_NAME = Regex(complete(STAGE_NAMING_REGEX), error='Invalid step name.')
EXEC = Regex(complete(EXEC_REGEX), error='Exec path should be patterned as "{module_path.py}:{exec_name}".')

STATIC_DAG_SCHEMA = Schema({
    dagmap_consts.STEPS_KEYNAME: {
            STEP_NAME: {
                dagmap_consts.EXEC_KEYNAME: EXEC,
                # Optional('params'): CONTEXT_SCHEMA,
                # Optional(dagmap_consts.INDEXED_INPUTS_KEYNAME): Or([OUTPUT], [INDEXED_OUTPUT], []),

                # Optional(dagmap_consts.NAMED_INPUTS_KEYNAME): Or({
                #     dagmap_consts.ALL_INPUTS_KEYNAME: [OUTPUT]
                # }, {
                #     OUTPUT_NAME: INDEXED_OUTPUT
                # }, {})
                Optional(dagmap_consts.DEPENDS_ON_KEYNAME): Or([STEP_NAME], []),
            }
        # },
        # Optional(dagmap_consts.DEPENDS_ON_KEYNAME): Or([STEP_NAME], []),
        # Optional(dagmap_consts.TAGS_KEYNAME): Or([TAG_NAME], [])
    }
})

def parse_schema(dag: dict, schema: Schema) -> dict:
    return schema.validate(dag)
