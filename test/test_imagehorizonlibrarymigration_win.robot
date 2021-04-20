*** Settings ***
Documentation   Test case to demonstrate ImageHorizonLibraryMigration keywords usage
...             Details: 
...    
...    

Library         ${CURDIR}/../migrate/ImageHorizonLibraryMigration.py  sikuli_path=sikulixide-2.0.5.jar
Library         OperatingSystem


*** Variables ***
${IMAGE_DIR}        ${CURDIR}/img/Windows
${DEFAULT_WAIT}     ${5}


*** Test Cases ***
Test Notepad With ImageHorizonLibraryMigration
    Set Log Level    TRACE
    log java bridge
    
    # local path for image files. images below have iNotepad prefix so that to differentiate from text Notepad
    imagePath add    ${IMAGE_DIR}

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
    #${prev}    settings set    MinSimilarity    ${0.7}
    set confidence    ${0.7}
    
    app open     C:/Windows/System32/notepad.exe
    
    wait for  iNotepad    ${DEFAULT_WAIT}
    click image  iNotepad

    set confidence    ${0.5}
    wait for  iNotepad mod
    click image  iNotepad

    app close    Notepad
    destroy vm
