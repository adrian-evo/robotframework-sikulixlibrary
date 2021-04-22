*** Settings ***
Documentation   Test case to demonstrate SikuliX library keywords usage
...             Install first with 'pip install robotframework-sikulixlibrary'
...             The reference images from img directory are generated on 1440 x 900 MacOS screen, Dark mode. Regenerate them for different environment
...

# Initialize library with sikuli_path or use SIKULI_PATH environment variable (recommended)
Library         SikuliXLibrary  sikuli_path=sikulixide-2.0.5.jar
#Library         SikuliXLibrary  sikuli_path=sikulixide-2.0.5.jar  image_path=  logImages=${True}  centerMode=${False}
Library         OperatingSystem


*** Variables ***
${IMAGE_DIR}        ${CURDIR}/img/MacOS
${DEFAULT_WAIT}     ${15}


*** Test Cases ***
Test TextEdit With SikuliX
    Set Log Level    TRACE
    log java bridge

    # local path for image files.
    imagePath add    ${IMAGE_DIR}

    set sikuli resultDir    ${OUTPUT DIR}
    Create Directory        ${OUTPUT DIR}/matches
    Create Directory        ${OUTPUT DIR}/screenshots

    region setAutoWait      ${DEFAULT_WAIT}
    # coordinates relative to upper left corner
    set offsetCenterMode    ${False}
    set notFoundLogImages   ${True}

    # for demo purpose
    settings setShowActions    ${True}
    ${prev}    settings set    Highlight            ${True}
    ${prev}    settings set    WaitAfterHighlight   ${0.5}

    # default min similarity
    ${prev}    settings set    MinSimilarity    ${0.9}

    # step 1
    log    Step1: open TextEdit
    app open     TextEdit
    region wait  NewDoc
    region click
    region wait  TextEdit  1

    #exit here

    # step 2
    # message is TextEdit2 not found after removing path
    log    Step2: TextEdit2 image should not be found
    imagePath remove  ${IMAGE_DIR}
    region exists     TextEdit2

    # step 3
    log    Step3: TextEdit2 should be found after adding image path
    imagePath add    ${IMAGE_DIR}
    region exists    TextEdit2

    region paste    Welcome to the all new SikuliX RF library
    sleep  3

    # step 4
    log     Step4: delete all typed text and type new one
    region type    text=A    modifier=SikuliXJClass.Key.CTRL
    region type    SikuliXJClass.Key.DELETE

    region paste   Welcome to the all new SikuliX RF libraryy    TextEdit edited=0.7    14    60
    region wait    TextEdit typed
    region type    SikuliXJClass.Key.BACKSPACE

    # step 5
    log    Step5: get all region text by OCR
    ${text}     region text    TextEdit typed
    log  ${text}

    # step 6
    log    Step6: type new line and new text
    region type    SikuliXJClass.Key.ENTER

    ${py4j}  Get Environment Variable  SIKULI_PY4J  default=0
    Run Keyword If  '${py4j}' == '1'
    ...    region paste   Based on Py4J Python module
    ...    ELSE    region paste   Based on JPype Python module

    #${prev}    settings set    Highlight        ${False}

    # step 7
    log    Step7: search and highlight Untitled text
    ${found}    region existsText    Format
    log  ${found}
    region highlight    3
    region highlightAllOff

    # step 8
    log    Step8: right click on TextEdit - will fail if SKIP is not used next
    region setFindFailedResponse    SKIP
    region rightClick    TextEdit    48    14
    sleep  3

    # step 9
    log    Step9: use correct image for right click
    region setFindFailedResponse    ABORT
    ${prev}    settings set    MinSimilarity    ${0.7}
    #region rightClick    TextEdit typed    48    14

    # coordinates relative to upper left corner of the image
    region click    TextEdit menu    338    8
    region click    TextEdit window    48    10
    
    region click    TextEdit menu    338    8

    # step 10
    # coordinates relative to center of the image
    log    Step10: same as step 9, with coordinates relative to center
    set offsetCenterMode    ${True}
    region click    TextEdit window2    -128    116

    # step 11
    log    Step11: dragDrop TextEdit
    set offsetCenterMode    ${False}
    ${prev}    settings set    DelayBeforeDrop    ${2.0}
    region dragDrop    TextEdit typed  TextEdit typed    60    12    110    12

    # step 12
    log    Step12: delete everything and close TextEdit
    region type    text=A    modifier=SikuliXJClass.Key.CTRL
    region type    SikuliXJClass.Key.DELETE

    app close    TextEdit
    destroy vm
    
*** Keywords ***
Exit Here
    app close    TextEdit
    destroy vm
    pass execution  .
