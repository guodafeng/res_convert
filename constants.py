
ACCOUNT = "Account"
PROJECT = "Project"
FEATURE = "Feature"
TEXTID = "TextID"
AREA = "Area"
SUBAREA = "Subarea"
DESCRIPTION = "Description"
COMMENT = "Comment"
LAYOUT = "Layout"
TERMS = "Terms"
ENGLISHGB = "English-GB"
LANGCODE = "LangCode"
TRANSLATION = "Translation"
# Columns below are not in DB table
SOURCEID = "ID-In-Source"
SOURCEPATH = "Path-of-Source"

TITLE_ROW = 3
# Source columns
SOURCES_COLUMNS = (
            ACCOUNT,
            PROJECT,
            FEATURE,
            TEXTID,
            AREA,
            SUBAREA,
            LAYOUT,
            TERMS,
            DESCRIPTION,
            ENGLISHGB,
            COMMENT,
            SOURCEID,
            SOURCEPATH
            )
        
# Translation columns
TRANSLATIONS_COLUMNS = (
            ACCOUNT,
            PROJECT,
            FEATURE,
            TEXTID,
            LANGCODE,
            TRANSLATION
            )

def col_in_xlsx(columns, start = 'A'):
    """
    columns: array of column names
    start: start column in xlsx
    return mapping of colum name to column in xlsx
    """
    col_map = {}
    col_num = ord(start)
    for col in columns:
        col_map[col] = chr(col_num)
        col_num += 1
    return col_map


