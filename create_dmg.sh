#!/bin/bash

# 设置变量
APP_NAME="NaviParser"
VERSION="1.0.0"
DMG_NAME="${APP_NAME}-v${VERSION}-macOS-universal"
APP_PATH="dist/${APP_NAME}.app"
DMG_PATH="dist/${DMG_NAME}.dmg"
VOLUME_NAME="${APP_NAME} ${VERSION}"
BACKGROUND_FILE="resources/dmg_background.png"

# 确保目标文件不存在
rm -f "${DMG_PATH}"

# 创建 DMG
create-dmg \
  --volname "${VOLUME_NAME}" \
  --volicon "resources/${APP_NAME}.icns" \
  --background "${BACKGROUND_FILE}" \
  --window-pos 200 120 \
  --window-size 660 400 \
  --icon-size 100 \
  --icon "${APP_NAME}.app" 180 170 \
  --hide-extension "${APP_NAME}.app" \
  --app-drop-link 480 170 \
  --no-internet-enable \
  "${DMG_PATH}" \
  "${APP_PATH}"

# 输出结果
echo "DMG created at: ${DMG_PATH}" 