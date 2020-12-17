*** Settings ***
Documentation   Test case to demonstrate SikuliLibraryMigration keywords usage
...             Details: 
...    
...    

Library         ${CURDIR}/../migrate/SikuliLibraryMigration.py
Library         OperatingSystem


*** Variables ***
${IMAGE_DIR}        ${CURDIR}/img
${DEFAULT_WAIT}     ${5}


*** Test Cases ***
Test Notepad With SikuliLibraryMigration
    Set Log Level    TRACE
    
    # local path for image files. images below have iNotepad prefix so that to differentiate from text Notepad
    add image path    ${IMAGE_DIR}

    set sikuli resultDir    ${OUTPUT DIR}
    Create Directory        ${OUTPUT DIR}/matches
    Create Directory        ${OUTPUT DIR}/screenshots    

    region setAutoWait      ${DEFAULT_WAIT}
    # coordinates relative to upper left corner
    #set offsetCenterMode    ${False}
    set notFoundLogImages   ${True}
    
    # for demo purpose
    settings setShowActions    ${True}
    ${prev}    settings set    Highlight            ${True}
    ${prev}    settings set    WaitAfterHighlight   ${0.9}

    # default min similarity
    ${prev}    settings set    MinSimilarity    ${0.7}

    app open     C:/Windows/System32/notepad.exe

    wait until screen contain  iNotepad    ${DEFAULT_WAIT}
    click  iNotepad
    wait until screen not contain  iNotepad mod    ${DEFAULT_WAIT}
    
    exists  iNotepad
    exists  iNotepad mod=0.6
    click  iNotepad
    
    ${text}  get text  iNotepad    

    app close    Notepad
    #destroy vm
