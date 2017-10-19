
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
OLDID = "OLD_ID"

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

# T2 Source columns
T2_SOURCES_COLUMNS = (
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
            OLDID
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

def col_in_xlsx(columns):
    """
    columns: array of column names
    start: start column in xlsx
    return mapping of colum name to column index as format 'A','C'..'AA'
    """
    start = 'A'
    def to_excel_column(col_index):
        low_bit = chr(ord(start) + col_index % 26)
        high_nums = col_index // 26
        if high_nums > 0:
            return to_excel_column(high_nums-1) + low_bit
        else:
            return low_bit

    col_map = {}
    for col_index, col in enumerate(columns):
        col_map[col] = to_excel_column(col_index)

    return col_map

def test_col_in_xlsx():
    testcols = [i for i in range(1000)]
    print(constants.col_in_xlsx(testcols))

