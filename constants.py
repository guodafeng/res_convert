
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
MANDATORYTRANSLATIONS_COLUMNS = (
            ACCOUNT,
            PROJECT,
            FEATURE,
            TEXTID,
            LANGCODE,
            TRANSLATION
            )

