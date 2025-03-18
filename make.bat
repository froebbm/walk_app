:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: VARIABLES                                                                    :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
SETLOCAL
SET ENV_NAME=walk_app

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: COMMANDS                                                                     :
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Jump to command
GOTO %1

:: Build the local environment from the environment file
:env
    ENDLOCAL & (
        :: Install MAMBA for faster solves
        CALL conda install -c conda-forge mamba 
        :: Install yaml
        CALL mamba install -c conda-forge pyyaml
        :: update environment with package dependencies
        CALL python check_package_deps.py --package
        :: Create new environment from environment file
        CALL mamba env create -f build_environment.yml
        :: Activate the environment so you can get to work
        CALL activate %ENV_NAME%
        :: Install the local package in development (experimental) mode
        CALL python -m pip install -e .
    )
    EXIT /B

:: Activate the environment
:env_activate
    ENDLOCAL & CALL activate %ENV_NAME%
    EXIT /B

:: Remove the environment
:env_remove
	ENDLOCAL & (
		CALL conda deactivate
		CALL conda env remove --name %ENV_NAME% -y
		CALL activate
	)
	EXIT /B


EXIT /B