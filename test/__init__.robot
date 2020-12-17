*** Settings ***
Documentation   Suite setup in case all tests from this directory should be run as a suite
...    

Suite Setup     SikuliX Suite Setup
Suite Teardown  SikuliX Suite Teardown


*** Keywords ***
SikuliX Suite Setup
    Log  SikuliX suite setup


SikuliX Suite Teardown
    Log  SikuliX suite teardown