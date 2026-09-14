#!/bin/bash
set -e

# 允許本機 X11 顯示連接
xhost +local:root > /dev/null 2>&1 || true

# 檢查 NVIDIA GPU 與驅動是否正常運作
GPU_FLAG=""
if nvidia-smi &> /dev/null; then
    echo "[run.sh] 檢測到可用 NVIDIA GPU，啟用 GPU 加速模式 (--gpus all)"
    GPU_FLAG="--gpus all"
else
    echo "[run.sh] 未檢測到可用 NVIDIA 驅動或 GPU，啟用 Mesa / DRI CPU 渲染模式"
fi

# 檢查是否有 DRI 設備以支援 Intel / AMD / 軟體 Mesa 加速
DRI_FLAG=""
if [ -d /dev/dri ]; then
    DRI_FLAG="--device /dev/dri:/dev/dri"
fi

# 如果未建置映像檔，提示先建置
if [[ "$(docker images -q guanxin_sim:latest 2> /dev/null)" == "" ]]; then
    echo "[run.sh] 找不到 guanxin_sim:latest 映像檔，開始自動執行建置..."
    docker build -t guanxin_sim:latest .
fi

# ==================== 汽車模組開關解析 (Vehicle Switch Option) ====================
ENABLE_CAR=""
CUSTOM_COMMAND=()

# 優先檢查環境變數
if [[ -n "${ENABLE_CAR}" ]]; then
    if [[ "${ENABLE_CAR}" == "0" || "${ENABLE_CAR}" == "false" || "${ENABLE_CAR}" == "no" ]]; then
        ENABLE_CAR="false"
    else
        ENABLE_CAR="true"
    fi
elif [[ -n "${WITH_CAR}" ]]; then
    if [[ "${WITH_CAR}" == "0" || "${WITH_CAR}" == "false" || "${WITH_CAR}" == "no" ]]; then
        ENABLE_CAR="false"
    else
        ENABLE_CAR="true"
    fi
fi

# 解析命令列參數
while [[ $# -gt 0 ]]; do
    case "$1" in
        --no-car|--map-only|-m|--map|--no-vehicle)
            ENABLE_CAR="false"
            shift
            ;;
        --car|--with-car|-c|--vehicle)
            ENABLE_CAR="true"
            shift
            ;;
        --help|-h)
            echo "================================================================="
            echo "  關新路自駕與街區模擬啟動腳本 (Hsinchu Guanxin Sim Launcher)"
            echo "================================================================="
            echo "用法: $0 [選項] [自訂指令]"
            echo ""
            echo "選項 (汽車模組開關):"
            echo "  --car, -c, --with-car       開啟汽車模組 (載入 Model Y、相機串流、鍵盤操控視窗)"
            echo "  --no-car, -m, --map-only    關閉汽車模組 (純地圖檢視/編輯模式：僅啟動 Gazebo 世界)"
            echo "  --help, -h                  顯示此說明訊息"
            echo ""
            echo "環境變數控制:"
            echo "  ENABLE_CAR=0 $0             以純地圖模式啟動"
            echo "  ENABLE_CAR=1 $0             以完整車輛模擬模式啟動"
            echo ""
            echo "常用執行範例:"
            echo "  $0                          預設啟動 (若在終端會提示選擇模式，6秒預設開啟汽車)"
            echo "  $0 -m                       直接以地圖純檢視模式啟動 (不載入汽車)"
            echo "  $0 -c                       直接以完整模擬模式啟動 (含 Model Y 與操控)"
            echo "  $0 bash                     進入容器 Bash 互動終端"
            echo "================================================================="
            exit 0
            ;;
        *)
            CUSTOM_COMMAND+=("$1")
            shift
            ;;
    esac
done

# 若使用者未指定自訂指令，且尚未決定開關：
if [ ${#CUSTOM_COMMAND[@]} -eq 0 ]; then
    if [ -z "$ENABLE_CAR" ]; then
        if [ -t 0 ]; then
            # 互動終端模式：提供選單開關詢問
            echo "================================================================="
            echo "  🚗 關新路模擬系統啟動選項 (請選擇是否開啟汽車模組)"
            echo "================================================================="
            echo "  [1] 完整模擬模式 (開啟汽車模組: 載入 Model Y、相機視窗、鍵盤操控)"
            echo "  [2] 地圖純檢視模式 (關閉汽車模組: 僅載入街區世界，平常改地圖專用)"
            echo "================================================================="
            read -t 6 -p "請選擇啟動模式 [1/2] (預設 1，6 秒後自動啟動): " MODE_CHOICE || MODE_CHOICE=""
            echo ""
            case "$MODE_CHOICE" in
                2|m|map|no|false)
                    ENABLE_CAR="false"
                    ;;
                *)
                    ENABLE_CAR="true"
                    ;;
            esac
        else
            # 非互動終端 (如背景任務或腳本)：預設開啟汽車模組
            ENABLE_CAR="true"
        fi
    fi

    if [ "$ENABLE_CAR" = "true" ]; then
        echo "[run.sh] 🚀 啟動模式: 【完整模擬模式】(已開啟汽車模組: Model Y + 相機視窗 + 鍵盤操控)"
    else
        echo "[run.sh] 🗺️ 啟動模式: 【地圖純檢視模式】(已關閉汽車模組: 僅載入世界，適合編輯與檢視地圖)"
    fi
    COMMAND="ros2 launch guanxin_sim sim.launch.py enable_vehicle:=$ENABLE_CAR"
else
    COMMAND="${CUSTOM_COMMAND[*]}"
    echo "[run.sh] 執行自訂指令: $COMMAND"
fi

echo "[run.sh] 正在啟動 guanxin_sim_container..."

docker run -it --rm \
    $GPU_FLAG \
    $DRI_FLAG \
    --net=host \
    --ipc=host \
    -e DISPLAY="${DISPLAY:-:0}" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v "$(pwd)/src:/ros2_ws/src" \
    --name guanxin_sim_container \
    guanxin_sim:latest \
    bash -c "source /opt/ros/jazzy/setup.bash && colcon build --symlink-install > /dev/null && source /ros2_ws/install/setup.bash && $COMMAND"
