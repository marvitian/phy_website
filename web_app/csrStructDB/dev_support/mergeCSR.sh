#!/bin/bash

# ------------------------------------------------------
# Dependancies
#   1. Script exists in CSRINIT/dpi
#   2. csrStructGen.sh exists in wd
#   3. VERIFICATION exists
#       3.1 run_log
#   4. inputs/cfg3 exists with the correct directory structure
#   5. Script must be run from the dpi directory

# ------------------------------------------------------


#required arguments
#   cfg, speed_fsp0, speed_fsp1, protocol, board_setup, rate
set -e

## csrStructGen args
PROTOCOL=""
BOARD_SETUP=""
PHY_CFG=""
RATE=""
OUTPUT=""
NUM_FSP=1
DBI_STRING="off"
DMD_STRING="on"
FUNCTIONAL_MODE=0
FUNCTIONAL_TEST=0
STRUCT_EXTRA_ARGS=""

## Path variables
SCR_PTH=$(dirname "$(realpath $0)")
# TRUNK="$(dirname -- "$(realpath -- "$(dirname "$SCR_PTH")")")"
DPI_PTH=${SCR_PTH}
GEN_PTH="../../VERIFICATION/simulation/phy_tb/sim/"
VRIF_PTH="../../VERIFICATION/source/phy_tb/tests_c/"

## Log file and Key log
LOG_PTH=""                                  # Script log
# KEY_LOG=""                                  # Log file for storing added and omitted keys for each speed

declare -a INPUT_SPDS_ARR
declare -a REAL_SPDS           # All speeds after rounding down(if any); used for running gen and sim scripts
declare -a ALL_ORD

declare -a INPUT_PAIRS_ARR
declare -a REAL_PAIR_SPDS
declare -a PAIR_ORD

declare -a INPUT_SNGL_ARR
declare -a REAL_SNGL_SPDS
declare -a SNGL_ORD

## Internal vars
OVR_KEYS=""
OVR_VALS=""
GEN_OFF=0
VRIF_OFF=0
LP4_RANGE_EDGES="1600,3200"

CLEAN=0

## Checks invalid arguments and sets internal vars
function process_arguments {
    while [ -n "$1" ]
    do
        echo "$1"
        case $1 in
            -protocol) PROTOCOL=$2; shift;;
            -board_setup)   BOARD_SETUP=$2; shift ;;
            -phy_cfg)       PHY_CFG=$2; shift ;;
            -rate)          RATE=$2; shift ;;
            -single_spd)    SINGLE_SPD=$2; shift ;;
            -num_fsp)       NUM_FSP=$2; shift ;;
            -spd_pairs)     SPD_PAIRS=$2; shift ;;
            -ovr_keys)      OVR_KEYS=$2; shift;;
            -ovr_vals)      OVR_VALS=$2; shift ;;
            -output)        OUTPUT=$2; shift ;;
            -gen_off)       GEN_OFF=1; shift;;   
            -vrif_off)      VRIF_OFF=1; shift;;
            -clean)         CLEAN=1;;
            -input)         NEW_INPUT=$2; shift ;;
            -vrif_dir)      VRIF_DIR=$2; shift ;;
            -mem_model) STRUCT_EXTRA_ARGS+="$1 $2 "; shift;;
			-test) STRUCT_EXTRA_ARGS+="$1 $2 "; shift;;
			-dbi) STRUCT_EXTRA_ARGS+="$1 "; DBI_STRING="on";;
			-dmd_off) STRUCT_EXTRA_ARGS+="$1 "; DMD_STRING="off";;
			-dq_odt) STRUCT_EXTRA_ARGS+="$1 $2 "; shift;;
			-ca_odt) STRUCT_EXTRA_ARGS+="$1 $2 "; shift;;
			-cs_odt) STRUCT_EXTRA_ARGS+="$1 $2 "; shift;;
			-latency) STRUCT_EXTRA_ARGS+="$1 $2 "; shift;;
			-no_ch) STRUCT_EXTRA_ARGS+="$1 $2 "; shift;;
			-seed) STRUCT_EXTRA_ARGS+="$1 $2 "; shift;;
			-default) STRUCT_EXTRA_ARGS+="$1 "; shift;;
			-bump_map) STRUCT_EXTRA_ARGS+="$1 "; shift;;
			-functional_mode) STRUCT_EXTRA_ARGS+="$1 "; shift;;
			-functional_test) STRUCT_EXTRA_ARGS+="$1 "; shift;;
			-quiet) STRUCT_EXTRA_ARGS+="$1 "; shift;;
			-help)
                echo 
                echo
                echo "	This script generates, merges, and verifies csrInitStructs"
                echo 
                echo "Mandatory Arguments:"
                echo "-output OUT                     OUT is the output directory for generated and merged files, log files, and key summaries."
                echo "-single_spd S1,S2,S3...         List of individual speeds that are to be merged."
                echo "-spd_pairs S1,S2,S3,S4...       List of speed pairs to be merged, S1 and S2 are pairs where S1 is on fsp0 and S2 is on fsp 1."
                echo "  **either single_spd or spd_pairs, or both, must be provided"
                echo 
                echo "Mandatory csrStructGen Arguments:"
                echo "-protocol PROT			PROT is the LP-protocol. Can be 4 or 5, do not add lp suffix. Illegal forms LP4, LP4x, LP5, or LP5x."
                echo "-board_setup SET		SET is the board setup. Can be 8 or 16. Illegal forms X8, X16, x8 or x16."
                echo "-rate RATE			RATE is the dfi to ck ratio."
                echo "-phy_cfg CFG			CFG is the PHY configuration."
                echo 
                echo "Other Arguments:"
                echo "-ovr_keys KEY1,KEY2,...         List of keys to be overwritten before simulation."
                echo "-ovr_vals KEY1,KEY2,...         List of values for the respective keys passed to ovr_keys."
                echo "-gen_off                        Disables csrInitStruct generation."
                echo "-vrif_off                       Disables csrInitStruct verification."
                echo "-input INPUT_PTH, RUN_LOG       INPUT_PTH is the path to the inputs folder containing the csrInitStruct.txt files to use as input. Default path is ...dpi/inputs/"
                echo "                                 RUN_LOG is the path to the run_log folder containing run logs generated by csrStructGen.sh. Default path is ...VERIFICATION/simulation/phy_tb/sim/run_log."
                echo "-vrif_dir PTH                     PTH is the path to the VERIFICATION folder. This folder must contain the correct subdirectories . Default is ../../VERIFICATION."
                echo "-clean                            Removes all existing files in output directory."
                echo
                echo "Other csrStructGen Arguments: passed directly to csrStructGen.sh script"
                echo "-num_fsp NFSP                   NFSP is the number of fsps to include in output file, this can be 1(fsp0) or 2(fsp0 and fsp1). Default value is 1"
                echo "-test FILE			FILE is a file within VERIFICATION/source/phy_tb/tests_sv/debug_tests."
                echo "-mem_model MEM			MEM is the memory  mode used. Default value is mic_lp4_2x16 for LP4, and mic_lp5_32 for LP5"
                echo "-dq_odt ODT			ODT is the value given to the csr_DQODT parameter. Default value is 4"
                echo "-ca_odt ODT			ODT is the value given to the csr_CAODT parameter. Default value is 4"
                echo "-cs_odt ODT			ODT is the value given to the csr_CSODT parameter. Default value is 4"
                echo "-latency WL			WL is the value give to the WL latency set parameter. Default value is 0"
                echo "-dbi				Enable DBI Read and DBI Write. Takes no argument. Default value is OFF"
                echo "-dmd_off			Disable DMD. Takes no argument. By default DMD is ON"
                echo "-functional_mode		Enables keys labeled FUCNTIONAL_MODE"
                echo "-functional_test		Enables keys labeled FUNCTIONAL_TEST"
                echo "-bump_map			Enable Bump Map Keys. Takes no argument. By default Bump Map keys are disbled"
                echo "-quiet				Disables most command line outputs, but will still generate all log files. Takes no argument"
                echo "-help				Displays the current message"
                echo
                # echo "eg."
                # echo "./csrStructGen.sh -protocol lp5 -board_setup x16 -phy_cfg 10 -speed_range 4800-5200 -step_size 128 -dbi"
                # echo 
                # echo "The output of this file is placed in it's associated directory within CSRINIT/dpi/inputs/"
                echo
                echo
                exit 1
                ;;
            *) 
                echo "Invalid option $1, use './csrStructGen.sh -help' for help"; exit 1;;
        esac
        shift
    done
    echo "SNDJKFSNJDKF"
    # print_paths
    ## Validate Dependancies
    #   1. Script exists in trunk/CSRINIT/dpi
    #   3. trunk/VERIFICATION exists
    #       3.1 required subdirectories exist
    #   2. csrStructGen.sh exists in wd
    #   4. Script must be run from the dpi directory
    if !(grep -q "CSRINIT/dpi" <<< "$SCR_PTH"); then echo "Error: Merge script must be in CSRINIT/dpi."; exit 1; fi
    if [ "$VRIF_DIR" ]; then
        if [ ! -d ${VRIF_DIR} ]; then echo "Error: Invalid path '$VRIF_DIR' for VERIFICATION directory. "; exit 1 
        elif [ ! -d ${VRIF_DIR}/simulation/phy_tb/sim ]; then echo "Error: Missing VERIFICATION/simulation/phy_tb/sim/ directory."; exit 1
        elif [ ! -d ${VRIF_DIR}/source/phy_tb/tests_c ]; then echo "Error: Missing VERIFICATION/source/phy_tb/tests_c/ directory."; exit 1
        fi
        GEN_PTH="$VRIF_DIR/simulation/phy_tb/sim/"
        VRIF_PTH="$VRIF_DIR/VERIFICATION/source/phy_tb/tests_c/"   
    else
        if [ ! -d ../../VERIFICATION ]; then echo "Error: Missing ../../VERIFICATION directory."; exit 1 
        elif [ ! -d ../../VERIFICATION/simulation/phy_tb/sim ]; then echo "Error: Missing VERIFICATION/simulation/phy_tb/sim/ directory."; exit 1 
        elif [ ! -d ../../VERIFICATION/source/phy_tb/tests_c ]; then echo "Error: Missing VERIFICATION/source/phy_tb/tests_c/ directory."; exit 1 
        fi
        GEN_PTH="../../VERIFICATION/simulation/phy_tb/sim/"
        VRIF_PTH="../../VERIFICATION/source/phy_tb/tests_c/"   
    fi
    if [ ! -f $GEN_PTH"csrStructGen.sh" ]; then echo "Error: Missing csrStructGen.sh script, it must be in '$GEN_PTH'."; exit 1; fi
    if [ "$(pwd)" != "$SCR_PTH" ]; then echo "Error: Script must be run from $SCR_PTH."; exit 1; fi


    # ------------------------------------ Processing Arguments ------------------------------------ #
    # Mandatory Arguments
    if [ ! "$PROTOCOL" ] || [ ! "$BOARD_SETUP" ] || [ ! "$PHY_CFG" ] || [ ! "$RATE" ] || [ ! "$OUTPUT" ] || [ ! "$SINGLE_SPD" ] && [ ! "$SPD_PAIRS" ]; then
        echo "arguments protocol, board_setup, phy_cfg, rate, output, and either or both of single_spd and spd_pairs must be provided"
        echo "$usage" >&2; exit 1
    fi
    if [ "$PROTOCOL" != "4" ] && [ "$PROTOCOL" != "5" ]; then echo "Invalid protocol value of $PROTOCOL. It must be 4 or 5."; exit 1; fi
    if [ "$BOARD_SETUP" != "8" ] && [ "$BOARD_SETUP" != "16" ]; then echo "Invalid board setup value of $BOARD_SETUP. It must be 8 or 16."; exit 1; fi

    # SPD_PAIRS must recieve odd num of args
    if [ $(($(echo "$SPD_PAIRS" | tr ',' ' ' | wc -w)%2)) -ne 0 ]; then echo "INVALID NUMBER OF INPUTS FOR PAIRS"; exit 1; fi

    # Corner Cases
    if [ "$OUTPUT" = "." ]; then OUTPUT=$SCR_PTH
    elif [ "$OUTPUT" = ".." ]; then OUTPUT="$(realpath -- "$(dirname "$SCR_PTH")")"
    fi
    #OUTPUT, if it has / at the end, remove it ------- orrrrrrrrr keep it and change script?
    
    # Update Paths
    NEW_INPUT=(${NEW_INPUT//,/ })
    if [ "$NEW_INPUT" ]; then 
        if [ "${NEW_INPUT[0]}" = "${NEW_INPUT[1]}" ]; then
            echo "The 'inputs' folder cannot be the same as the 'run_log' folder. Change the paths passed to -input."; exit 1
        fi
        if [ $GEN_OFF -eq 1 ]; then
            if [ "${NEW_INPUT[0]}" = "." ]; then 
                INPUT_PTH=$SCR_PTH
            elif [ "${NEW_INPUT[0]}" = ".." ]; then 
                INPUT_PTH="$(realpath -- "$(dirname "$SCR_PTH")")"
            else 
                INPUT_PTH="${NEW_INPUT[0]}"
            fi
            if [ "${NEW_INPUT[1]}" = "." ]; then 
                RUN_LOG=$SCR_PTH
            elif [ "${NEW_INPUT[1]}" = ".." ]; then 
                RUN_LOG="$(realpath -- "$(dirname "$SCR_PTH")")"
            else 
                RUN_LOG="${NEW_INPUT[1]}"
            fi
        else    # default inputs/, VERIFICATION/simulation/phy_tb/sim/run_log
            INPUT_PTH="inputs/cfg${PHY_CFG}/lp${PROTOCOL//[!0-9]/}/x${BOARD_SETUP}/dfi2ck_${RATE}/dbi_${DBI_STRING}/dmd_${DMD_STRING}"
            RUN_LOG="../../VERIFICATION/simulation/phy_tb/sim/run_log"
            echo -e "WARNING: -gen_off not passed, argument -input_pth will be ignored. Default path $INPUT_PTH will be used.\n" | tee -a $LOG_PTH
        fi
    else 
        INPUT_PTH="inputs/cfg${PHY_CFG}/lp${PROTOCOL//[!0-9]/}/x${BOARD_SETUP}/dfi2ck_${RATE}/dbi_${DBI_STRING}/dmd_${DMD_STRING}"
        RUN_LOG="../../VERIFICATION/simulation/phy_tb/sim/run_log"
    fi
    INPUT_SPDS="$(echo "${SINGLE_SPD},${SPD_PAIRS}" | sed -r ':a; s/\b([[:alnum:]]+)\b(.*)\b\1\b/\1\2/g; ta;' | sed 's/,\{2,\}/,/g')"  #Removes Duplicates
    LOG_PTH="$OUTPUT/mergeCSR.log"
    KEY_LOG="$OUTPUT/keys_csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${INPUT_SPDS//,/_}Mbps.log"
    TMP_PTH="$OUTPUT/.tmp"

    if !([ "$NUM_FSP" = "1" ] || [ "$NUM_FSP" = "2" ]); then        # If fsp is not 1 or 2
        echo "Invalid Value for num_fsp"
        exit 1
    fi
    if [ "$NUM_FSP" = "2" ] && [ ! "$SINGLE_SPD" ]; then            # If fsp is 2 and no args passed to single_spd 
        echo "num_fsp passed without any speeds, pass arguments to -single_spd"
        exit 1
    fi

    #Processing Speed Inputs; Round Down Values
    if [ "$SINGLE_SPD" ]; then
        for SPD in ${SINGLE_SPD//,/ }
        do
            if [[ "$LP4_RANGE_EDGES" == *"$SPD"* ]] || [[ "$LP5_RANGE_EDGES" == *"$SPD"* ]] ; then      # SPDS on range edges rounded down
                REAL_SPDS["$rl_cnt"]="$(($SPD-8))"; ALL_ORD+=( "$rl_cnt" )
                REAL_SNGL_SPDS["$cnt"]="$(($SPD-8))"; SNGL_ORD+=( "$cnt" )
            elif [ $((${SPD}%8)) -ne "0" ]; then 
                for ((j=$SPD; j>($SPD-10); j-=2))                                                       # Find nearest multiple of 8 that is < the speed
                do
                    if [ $((${j}%8)) -eq "0" ]; then 
                        REAL_SPDS["$rl_cnt"]="$j"; ALL_ORD+=( "$rl_cnt" )
                        REAL_SNGL_SPDS["$cnt"]="$j"; SNGL_ORD+=( "$cnt" )
                        break
                    fi
                done
            else 
                REAL_SPDS["$rl_cnt"]="$SPD"; ALL_ORD+=( "$rl_cnt" )
                REAL_SNGL_SPDS["$cnt"]="$SPD"; SNGL_ORD+=( "$cnt" )
            fi
            INPUT_SPDS_ARR["$rl_cnt"]="$SPD"; ALL_ORD+=( "$rl_cnt" )
            INPUT_SNGL_ARR["$cnt"]="$SPD"; SNGL_ORD+=( "$cnt" )
            cnt=$(($cnt + 1))
            rl_cnt=$(($rl_cnt + 1))
        done
    fi
    if [ "$SPD_PAIRS" ]; then
        cnt=0
        for SPD in ${SPD_PAIRS//,/ }
        do
            if [[ "$LP4_RANGE_EDGES" == *"$SPD"* ]] || [[ "$LP5_RANGE_EDGES" == *"$SPD"* ]] ; then      # SPDS on range edges rounded down
                REAL_SPDS["$rl_cnt"]="$(($SPD-8))"; ALL_ORD+=( "$rl_cnt" )
                REAL_PAIR_SPDS["$cnt"]="$(($SPD-8))"; PAIR_ORD+=( "$cnt" )
            elif [ $((${SPD}%8)) -ne "0" ]; then 
                for ((j=$SPD; j>($SPD-10); j-=2))                                                       # Find nearest multiple of 8 that is < SPD
                do
                    if [ $((${j}%8)) -eq "0" ]; then 
                        REAL_SPDS["$rl_cnt"]="$j"; ALL_ORD+=( "$rl_cnt" )
                        REAL_PAIR_SPDS["$cnt"]="$j"; PAIR_ORD+=( "$cnt" )
                        break
                    fi
                done
            else 
                REAL_SPDS["$rl_cnt"]="$SPD"; ALL_ORD+=( "$rl_cnt" )
                REAL_PAIR_SPDS["$cnt"]="$SPD"; PAIR_ORD+=( "$cnt" )
            fi
            INPUT_SPDS_ARR["$rl_cnt"]="$SPD"; ALL_ORD+=( "$rl_cnt" )
            INPUT_PAIRS_ARR["$cnt"]="$SPD"; PAIR_ORD+=( "$cnt" )

            # REAL_PAIR_SPDS["$cnt"]="$SPD"; PAIR_ORD+=( "$cnt" )
            cnt=$(($cnt + 1))
            rl_cnt=$(($rl_cnt + 1))
        done
    fi
    # print_arrs
    # Remove SPD Duplicates
    IFS=" " read -r -a REAL_SPDS <<< "$(echo "${REAL_SPDS[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ')"
    IFS=" " read -r -a INPUT_SPDS_ARR <<< "$(echo "${INPUT_SPDS_ARR[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ')"
    IFS=" " read -r -a REAL_SNGL_SPDS <<< "$(echo "${REAL_SNGL_SPDS[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ')"
    # IFS=" " read -r -a REAL_PAIR_SPDS <<< "$(echo "${REAL_PAIR_SPDS[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ')"
    
    # Sort Input and Real Speed arrays so they have the same order
    # REAL_SPDS=( $( printf "%s\n" "${REAL_SPDS[@]}" | sort -n ) )
    # INPUT_SPDS_ARR=( $( printf "%s\n" "${INPUT_SPDS_ARR[@]}" | sort -n ) )

    # Overwrite keys and vals must match
    # TODO: update so it also includes if number of values passed to each is unmatching
    if ([ ! "$OVR_KEYS" ] && [ "$OVR_VALS" ]) || ([ "$OVR_KEYS" ] && [ ! "$OVR_VALS" ]); then
        echo "Unmatching Overwrite keys and values, provide both key name and value."
        exit 1
    fi

    # Clean Output Directory
    if [ "$CLEAN" = "1" ] && [ "$(ls -A $OUTPUT)" ]; then
        rm -r ${OUTPUT}/*
    fi

}

# Debug function
function print_args {
    echo ""
    echo "protocol: $PROTOCOL"
    echo "board_setup: $BOARD_SETUP"
    echo "phy_cfg: $PHY_CFG"
    echo "rate: $RATE"
    echo "NUM_FSP: $NUM_FSP"
    echo "SINGLE_SPD: $SINGLE_SPD"
    echo "SPD_PAIRS: $SPD_PAIRS"
    echo "INPUT_SPDS: $INPUT_SPDS"
    echo "GEN_OFF: $GEN_OFF"
    echo "VRIF_OFF: $VRIF_OFF"
    echo "output: $OUTPUT"
    echo "struct_extra_args: $STRUCT_EXTRA_ARGS"
    echo ""
}
function print_paths {
    echo ""
    echo "SCR_PTH = $SCR_PTH"
    # echo "TRUNK = $TRUNK"
    echo "DPI_PTH = $DPI_PTH"
    echo "GEN_PTH = $GEN_PTH"
    echo "VRIF_PTH = $VRIF_PTH"
    echo "LOG_PTH = $LOG_PTH"
    echo "TMP_PTH = $TMP_PTH"
    echo "INPUT_PTH = $INPUT_PTH"
    echo "RUN_LOG = $RUN_LOG"
    echo ""
}
function print_arrs {
    echo "INPUT_SPDS_ARR = ${INPUT_SPDS_ARR[@]}"
    echo "REAL_SPDS = ${REAL_SPDS[@]}"
    echo "INPUT_SNGL_ARR = ${INPUT_SNGL_ARR[@]}"
    echo "REAL_SNGL_SPDS = ${REAL_SNGL_SPDS[@]}"
    echo "INPUT_PAIRS_ARR = ${INPUT_PAIRS_ARR[@]}"
    echo "REAL_PAIR_SPDS = ${REAL_PAIR_SPDS[@]}"
}

## Determines if a value exists in array
#   Args: $1: item to search for
#         $2: array to search in
function containsElement {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done    # 'for' without an 'in' implicitly iterates over the argument list (only arr cause we shifted arg list)
  return 1
}

function init {
    echo -e "==================\n\tArguments\n==================" > $LOG_PTH
    echo 
    echo -e "protocol: $PROTOCOL" | tee -a $LOG_PTH;
    echo -e "board_setup: $BOARD_SETUP" | tee -a $LOG_PTH;
    echo -e "phy_cfg: $PHY_CFG" | tee -a $LOG_PTH;
    echo -e "rate: $RATE" | tee -a $LOG_PTH;
    echo -e "input speeds: = ${INPUT_SPDS_ARR[@]}" | tee -a $LOG_PTH;
    echo -e "true speeds: = ${REAL_SPDS[@]}" | tee -a $LOG_PTH;
    echo -e "output: $OUTPUT" | tee -a $LOG_PTH;
    echo | tee -a $LOG_PTH;

    echo "=================================================================================";
    echo -e "  start time = $(date +'%Y/%m/%d__%H:%M:%S') HOSTNAME = ${HOSTNAME} USER = ${USER}"
    echo "=================================================================================";
    echo

    if [ "$CLEAN" = "1" ]; then echo -e "\tCleaning Output"; fi
    echo -e "==================\n\tSpeed List\n==================" >> $LOG_PTH
    for SPD in ${REAL_SNGL_SPDS[@]}; do echo -e "\t$SPD" >> $LOG_PTH; done
    for ((i=0; i<${#REAL_PAIR_SPDS[@]}; i+=2)); do echo -e "\t${REAL_PAIR_SPDS[$i]} : ${REAL_PAIR_SPDS[${i}+1]}" >> $LOG_PTH; done
  
  # Initialize log and temporary files
    echo "" > $TMP_PTH
    echo "# ----------------------------------------------------------------------------------------------------------- #" >> $KEY_LOG
    echo -e "\n\tThis file contains an outline of the included and omitted keys for all input speeds" >> $KEY_LOG
    echo -e "\t The keys are classified into 3 main categories, "  >> $KEY_LOG
    echo -e "\t   FUNCTIONAL_SPEC: The necessary key, such as, MajorSystemMode, MajorMode, etc." >> $KEY_LOG
    echo -e "\t   FUNCTIONAL_SPEC: Optional keys, such as, channel DMD and DMI keys." >> $KEY_LOG
    echo -e "\t   FUNCTIONAL_SPEC: Optional keys specifically for testing.\n" >> $KEY_LOG
  
  # Create necessary directories
    mkdir -p "$OUTPUT/src/lp$PROTOCOL/x$BOARD_SETUP/dfi2ck_$RATE"
    mkdir -p "$OUTPUT/merged"
    mkdir -p "$OUTPUT/sngl_speed"
}

#####################################################################
#####	Individual Struct Generation and Verification Functions	#####
#####################################################################

## Generates CsrInitStruct.txt files by running csrStructGen.sh 
#   If one speed fails the rest are generated, but program terminates at end of function
function gen_csrstruct {
    echo -e "\n# ------------------------------------------------- Generating csrInitStruct -------------------------------------------------- #" >> $LOG_PTH
    local FAILED_SPDS=""
    cd $GEN_PTH
    for SPD in ${REAL_SPDS[@]}
    do
        echo -e "========================================================\n\tGenerating csrInitStruct for Baud rate of ${SPD}Mbps\n========================================================" >> $LOG_PTH
        echo -e "\tGenerating csrInitStruct for $SPD Mbps"
        if containsElement "$SPD" "${REAL_SNGL_SPDS[@]}"; then  # single spd, include -num_fsp arg
            echo ./csrStructGen.sh -phy_cfg ${PHY_CFG} -protocol ${PROTOCOL} -board_setup ${BOARD_SETUP} -rate ${RATE} -speed ${SPD} -num_fsp $NUM_FSP ${STRUCT_EXTRA_ARGS} >> $LOG_PTH
            ./csrStructGen.sh -phy_cfg ${PHY_CFG} -protocol ${PROTOCOL} -board_setup ${BOARD_SETUP} -rate ${RATE} -speed ${SPD} -num_fsp $NUM_FSP ${STRUCT_EXTRA_ARGS} > $TMP_PTH
        else    #Generate Speed Pairs, num_fsp not specified fsp0 will have first speed and fsp1 will have second speed
            echo ./csrStructGen.sh -phy_cfg ${PHY_CFG} -protocol ${PROTOCOL} -board_setup ${BOARD_SETUP} -rate ${RATE} -speed ${SPD} ${STRUCT_EXTRA_ARGS} >> $LOG_PTH
            # ./csrStructGen.sh -phy_cfg ${PHY_CFG} -protocol ${PROTOCOL} -board_setup ${BOARD_SETUP} -rate ${RATE} -speed ${SPD} ${STRUCT_EXTRA_ARGS} > $TMP_PTH
        fi
        cat $TMP_PTH >> $LOG_PTH
        if !(grep -q 'Test Passed' $TMP_PTH); then
            echo -e "\t** FAILED to generate csrInitStruct for $SPD Mbps **" | tee -a $LOG_PTH
            FAILED_SPDS+="$SPD,"
        fi
    done

    # Terminate if any fail
    # if [ "$FAILED_SPDS" ]; then
    #     echo -e "Failed to Generate csrStructs for speeds $FAILED_SPDS" | tee -a $LOG_PTH
    #     echo "Check $LOG_PTH for more information"
    #     exit 1;
    # fi
}

### CsrInitStruct Verification
function vrif_csrstruct {
    echo -e "\n# ------------------------------------------------- Verifying csrInitStruct --------------------------------------------------- #" >> $LOG_PTH
    local FAILED_SPDS=""
    cd $DPI_PTH
    # make -f dpi.mk all CC=/home/cds_user/cadence/xcelium1909_001/tools/cdsgcc/gcc/6.3/bin/g++ SW4=COMPILE_CFG$PHY_CFG -Werror >> $LOG_PTH
    echo make -f dpi.mk all CC=/home/cds_user/cadence/xcelium1909_001/tools/cdsgcc/gcc/6.3/bin/g++ SW4=COMPILE_CFG$PHY_CFG -Werror
    
    for SPD in ${REAL_SPDS[@]} 
    do
        echo -e "========================================================\n\tSimulating csrInitStruct for Baud rate of ${SPD}Mbps\n========================================================" >> $LOG_PTH
        echo -e "\tVerifying csrInitStruct for $SPD Mbps"
        # Step 2: Build
        cd $DPI_PTH
        echo ./output/CSRInit -i ${INPUT_PTH}/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt -o ref_data/cfg${PHY_CFG}/lp${PROTOCOL//[!0-9]/}/x${BOARD_SETUP}/dfi2ck_${RATE}/dbi_${DBI_STRING}/dmd_${DMD_STRING}/ref_csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt
        # ./output/CSRInit -i ${INPUT_PTH}/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt \
        # -o ref_data/cfg${PHY_CFG}/lp${PROTOCOL//[!0-9]/}/x${BOARD_SETUP}/dfi2ck_${RATE}/dbi_${DBI_STRING}/dmd_${DMD_STRING}/ref_csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt >> $LOG_PTH
        
        # Step 3: Simulation
        cd $VRIF_PTH
        echo ./csrStructSim.sh -test ref_data/cfg${PHY_CFG}/lp${PROTOCOL//[!0-9]/}/x${BOARD_SETUP}/dfi2ck_${RATE}/dbi_${DBI_STRING}/dmd_${DMD_STRING}/ref_csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt
        # ./csrStructSim.sh -test ref_data/cfg${PHY_CFG}/lp${PROTOCOL//[!0-9]/}/x${BOARD_SETUP}/dfi2ck_${RATE}/dbi_${DBI_STRING}/dmd_${DMD_STRING}/ref_csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt > $TMP_PTH
        cat $TMP_PTH >> $LOG_PTH
        if !(grep -q 'TEST PASSED' $TMP_PTH); then
            echo -e "\t** Simulation FAILED for $SPD Mbps **" | tee -a $LOG_PTH
            FAILED_SPDS+="$SPD,"
        fi
    done

    # # Terminate if any fail
    # if [ "$FAILED_SPDS" ]; then
    #     echo -e "csrInitStructs simulation failed for speeds $FAILED_SPDS" | tee -a $LOG_PTH
    #     echo "Check $LOG_PTH for more information"
    #     exit 1;
    # fi
}

#########################################
#####	Post Processing Functions	#####
#########################################

### writes keys_csrInitStruct_cfgX_LPX_xXX_SPD1_SPD2...Mbps.log ; outlines the included and omitted keys for each speed
# NOTE: iteration will be using indexes cause I might need to get both INPUT_SPDS and REAL_SPDS
#   Args: $1 the speed for which to log
function key_loger {
    cd $SCR_PTH
    # echo "$1"
    local SPD="$1"
    grep "\[KEY=VALUE, LABEL\]" $RUN_LOG/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt > $TMP_PTH #PUT ALL KEYS INTO FILE
    sed -i "s/.*--- //g" $TMP_PTH # REMOVE SUBSCRIPT 

  ## Log Included Keys
    echo -e "=========================\n\tKEYS FOR $SPD Mbps\n=========================" >> $KEY_LOG
    echo -e "\tEXISTING KEYS: " >> $KEY_LOG
    echo -e "\t\tFUNCTIONL_SPEC Keys:" >> $KEY_LOG

    if (containsElement "$SPD" "${REAL_SNGL_SPDS[@]}" && [ "$NUM_FSP" -eq "2" ]); then                                         # fsp1 included for single spd
        echo -e "$(awk "/FUNCTIONAL_SPEC/" $TMP_PTH)" | sed "s/, .*//g" | sed -e 's/^/\t\t\t/' >> $KEY_LOG                   # log FUNCTIONAL_SPEC keys with both fsp0 and fsp 1
    else
        echo -e "$(awk "/FUNCTIONAL_SPEC/" $TMP_PTH | awk "/MajorSystemMode.*/{p++}p==1")" | sed "s/, .*//g" | sed -e 's/^/\t\t\t/' >> $KEY_LOG # log FUNCTIONAL_SPEC keys with only fsp0
    fi

    if [ "$FUNCTIONAL_MODE" -eq "1" ]; then
        echo -e "\t\tFUNCTIONL_MODE Keys:" >> $KEY_LOG
        echo -e "$(grep "FUNCTIONAL_MODE" $TMP_PTH)" | sed "s/, .*//g" | sed -e 's/^/\t\t\t/' >> $KEY_LOG                    # log FUNCTIONAL_MODE keys
    fi
    if [ "$FUNCTIONAL_TEST" -eq "1" ]; then
        echo -e "\t\tFUNCTIONL_TEST Keys:" >> $KEY_LOG
        echo -e "$(grep "FUNCTIONAL_TEST" $TMP_PTH)" | sed "s/, .*//g" | sed -e 's/^/\t\t\t/' >> $KEY_LOG                    # log FUNCTIONAL_TEST keys"
    fi
    
    # Log Omitted Keys
    echo -e "\n\tOMITTED KEYS:" >> $KEY_LOG
    if (containsElement "$SPD" "${REAL_SNGL_SPDS[@]}" && [ "$NUM_FSP" -eq "1" ]) || (containsElement "$SPD" "${REAL_PAIR_SPDS[@]}"); then # fsp1 excluded for single speeds if number of fsps is 1
        echo -e "\t\tFUNCTIONL_SPEC Keys:" >> $KEY_LOG
        echo -e "$(awk "/FUNCTIONAL_SPEC/" $TMP_PTH | awk "/MajorSystemMode.*/{p++}p==2")" | sed "s/, .*//g" | sed -e 's/^/\t\t\t/' >> $KEY_LOG  ## log FUNCTIONAL_MODE keys
    fi
    if [ "$FUNCTIONAL_MODE" -eq "0" ]; then
        echo -e "\t\tFUNCTIONL_MODE Keys:" >> $KEY_LOG
        echo -e "$(grep "FUNCTIONAL_MODE" $TMP_PTH)" | sed "s/, .*//g" | sed -e 's/^/\t\t\t/' >> $KEY_LOG ## log FUNCTIONAL_MODE keys
    fi
    if [ "$FUNCTIONAL_TEST" -eq "0" ]; then
        echo -e "\t\tFUNCTIONL_TEST Keys:" >> $KEY_LOG
        echo -e "$(grep "FUNCTIONAL_TEST" $TMP_PTH)" | sed "s/, .*//g" | sed -e 's/^/\t\t\t/' >> $KEY_LOG ## log FUNCTIONAL_TEST keys"
    fi

    echo -e "\n" >> $KEY_LOG
}

### Calls key_loger function to log single speeds and speed pairs seperatedly 
function log_keys {
    echo -e "\tLogging Keys: view file at $KEY_LOG" | tee -a $LOG_PTH
    echo -e "# ---------------------------------------------- Single Speeds ---------------------------------------------- #" >> $KEY_LOG
    for SPD in ${REAL_SNGL_SPDS[@]}; do key_loger $SPD; done
    echo -e "# ---------------------------------------------- Speed Pairs ---------------------------------------------- #" >> $KEY_LOG
    local -a REAL_PAIR_SPDS_SORTED          # Remove duplicates before logging keys
    IFS=" " read -r -a REAL_PAIR_SPDS_SORTED <<< "$(echo "${REAL_PAIR_SPDS[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' ')"
    for SPD in ${REAL_PAIR_SPDS_SORTED[@]}; do key_loger $SPD; done
}

### Merges csrStruct for speed pairs
function merge {
    # echo "------------------- MERGING -------------------"
    echo -e "\tMerging Files: view merged files at $OUTPUT/merged" | tee -a $LOG_PTH
    cd $DPI_PTH
    for ((i=0; i<${#REAL_PAIR_SPDS[@]}; i+=2))
    do
        # echo "REAL[i] = ${REAL_PAIR_SPDS[$i]}"
        # echo "INPUT_PAIRS_ARR[i] = ${INPUT_PAIRS_ARR[$i]}"
        # echo "REAL[i+1] = ${REAL_PAIR_SPDS[$i+1]}"
        # echo "INPUT_PAIRS_ARR[i+1] = ${INPUT_PAIRS_ARR[$i+1]}"
        echo -e "\t\tMerging ${REAL_PAIR_SPDS[$i]} Mbps and ${REAL_PAIR_SPDS[$i+1]} Mbps csrInitStructs" | tee -a $LOG_PTH
        FSP0_KEYS="$(cat $INPUT_PTH/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${REAL_PAIR_SPDS[$i]}Mbps.txt)"
        FSP1_KEYS="$(cat $INPUT_PTH/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${REAL_PAIR_SPDS[$i+1]}Mbps.txt)"
        echo -e "${FSP0_KEYS}\n${FSP1_KEYS//ch0_fsp0/ch0_fsp1}" > $OUTPUT/merged/csrInitStruct_LP${PROTOCOL}_x${BOARD_SETUP}_fsp0_${INPUT_PAIRS_ARR[$i]}Mbps_fsp1_${INPUT_PAIRS_ARR[$i+1]}Mbps.txt
    done
}

### Formats generated csrInitStruct files generated; overwrites given keys, removed duplicates, and moves Major/Minor mode keys to the top of the file
function frmt_keys {
    echo -e "\tFormating All Generated Keys" | tee -a $LOG_PTH
    echo -e "\t\tOverwriting Keys: $OVR_KEYS" >> $LOG_PTH
    echo -e "\t\tRemoving Duplicate Keys" >> $LOG_PTH
    echo -e "\t\tMoving Major/Minor Keys to the Top of the csrInitStruct File" >> $LOG_PTH
    FILES=(${OUTPUT}/merged/*)
    FILES+=(${OUTPUT}/sngl_speed/*) # Potential problem, existing LP5 for example files in folder
    # echo "FILES = ${FILES[@]}"

    for FILE in ${FILES[@]}
    do
        # echo "FILE = $FILE"
        # echo -e "========================================================\n\tParsing Keys for Baud rate of ${SPD}Mbps\n========================================================" | tee -a $LOG_PTH
        
    ## Overwrite Keys
        if [ "$OVR_KEYS" ]; then  # there's a key to overwrite\
            OVR_KEYS=(${OVR_KEYS//,/ })
            OVR_VALS=(${OVR_VALS//,/ })
            for ((i=0; i<${#OVR_KEYS[@]}; i+=1))
            do
                if !(grep -q "${OVR_KEYS[$i]} = " "$FILE"); then #Check that key exists
                    echo -e "Could not overwrite key ${OVR_KEYS[$i]}: KEY DOESN'T EXIT IN $FILE" | tee -a $LOG_PTH
                    exit 1
                fi
                # echo -e "\tOVR_KEYS[$i] = ${OVR_KEYS[$i]} \tOVR_VALS[$i] = ${OVR_VALS[$i]} \t ${OVR_KEYS[$i]} = ${OVR_VALS[$i]}"
                # echo "sed -i '/${OVR_KEYS[$i]}/c\\${OVR_KEYS[$i]} = ${OVR_VALS[$i]}' $FILE" #CHANGE
                sed -i "/${OVR_KEYS[$i]}/c\\${OVR_KEYS[$i]} = ${OVR_VALS[$i]}" $FILE

            done
        fi

    ## Remove Duplicates
        DUP_KEYS="MinorMode_iActiveRanks,Major4"   # Keys that usually get duplicated # TODO: Expand list
        for KEY in ${DUP_KEYS//,/ }
        do
            sed -i "/$KEY/c\\$(sed "/$KEY/!d;q" $FILE)" $FILE     # Set all subsequent occurances to the value of the first one
            # echo "sed -i "/$KEY/c\\"$(sed "/${KEY}/!d;q" $FILE)"" $FILE"
        done
        echo "$(awk '!seen[$0]++' $FILE)" > $FILE # delete duplicates
    
    ## Mv Minor/Major Keys to Top
        cat $FILE | awk '{print $0}' > $TMP_PTH 
        # cat $FILE
        # echo "$(cat $FILE | awk '{print $0}')"
        # sleep 10
        ln_num=$((1))    # line currently on
        lst_ln=$((0))    # last line that had Major/Minor
        while read ln; do
            if grep -q 'Minor\|Major' <<< "$ln"; then
                # echo "$ln  ln_num = $ln_num  lst_ln = $lst_ln"
                if !([ "$ln_num" = "$((lst_ln+1))" ]); then 

                    # echo -e "\tPROBLEM: ln_num = $ln_num  lst_ln = $lst_ln \tsed '$((${lst_ln}+2))i $ln'\tsed -i -e "$((${ln_num}+1))d""
                    sed -i "$((${lst_ln}+1))i $ln" $TMP_PTH
                    # echo "ADDED"
                    sed -i -e "$((${ln_num}+1))d" $TMP_PTH
                    # echo "REOMVED"
                fi
                lst_ln=$((lst_ln+1))
                # lst_ln=${ln_num}
            fi
            ln_num=$((ln_num+1))
        done <$FILE
        # sleep 10
        mv $TMP_PTH $FILE
    done
    
}

#####################
#####	Main	#####
#####################

process_arguments "$@"
echo "DONE"
print_args
echo "DONE2"
init
# print_paths
# print_arrs

### Generate csrInitStructs for Given Rates
if [ $GEN_OFF -eq 0 ]; then 
    gen_csrstruct
else
    for SPD in ${REAL_SPDS[@]}  # Verify that necessary csrInitStruct.txt files are available
    do
        if [ ! -f $INPUT_PTH/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt ]; then
            echo "File csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt is missing from input folder '$INPUT_PTH'." | tee -a $LOG_PTH; exit 1
        fi
        if [ ! -f $RUN_LOG/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt ]; then
            echo "File $RUN_LOG/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${SPD}Mbps.txt is missing from run_log folder '$RUN_LOG'." | tee -a $LOG_PTH; exit 1
        fi
    done
fi
echo 

### Verify Generated Keys
if [ $VRIF_OFF -eq 0 ]; then vrif_csrstruct; fi
echo

echo -e "\n# ----------------------------------------------- Postprocessing csrInitStruct ------------------------------------------------ #" >> $LOG_PTH
### Log Included and Omitted Keys for All Speeds
log_keys

### Copy All Generated csrInitStructs to src directory
for ((i=0; i<${#REAL_SPDS[@]}; i++))
do  
    # echo "cp $INPUT_PTH/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${REAL_SPDS[$i]}Mbps.txt \
    # $OUTPUT/src/lp$PROTOCOL/x$BOARD_SETUP/dfi2ck_$RATE/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${REAL_SPDS[$i]}Mbps.txt"
    cp $INPUT_PTH/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${REAL_SPDS[$i]}Mbps.txt \
    $OUTPUT/src/lp$PROTOCOL/x$BOARD_SETUP/dfi2ck_$RATE/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${REAL_SPDS[$i]}Mbps.txt
done 

### Copy Single Speeds Into Output Dir
for ((i=0; i<${#REAL_SNGL_SPDS[@]}; i++))
do
    # echo "cp ${INPUT_PTH}/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${REAL_SNGL_SPDS[$i]}Mbps.txt ${OUTPUT}/sngl_speed/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${INPUT_SNGL_ARR[$i]}Mbps.txt"
    cp ${INPUT_PTH}/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${REAL_SNGL_SPDS[$i]}Mbps.txt ${OUTPUT}/sngl_speed/csrInitStruct_cfg${PHY_CFG}_LP${PROTOCOL}_x${BOARD_SETUP}_${INPUT_SNGL_ARR[$i]}Mbps.txt
done

### Merge File Pairs
merge

### Format Output Keys
frmt_keys

echo -e "\nCOMPLETE" | tee -a $LOG_PTH