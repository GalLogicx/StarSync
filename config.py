# config.py

# Является интеллектуальной собственностью и всецело принадлежит GalLogicx. Все права защищены. Любое несанкционированное использование или воспроизведение строго запрещено
# This is the intellectual property of and is entirely owned by GalLogicx. All rights reserved. Any unauthorized use or reproduction is strictly prohibited

THEMES = {
    "dark": {"bg": "#2D2F4D", "fg": "white", "logs": "#D9D9D9", "btn_text": "white"},
    "light": {"bg": "#FFF6E5", "fg": "#5d4037", "logs": "#FFDAB5", "btn_text": "#5d4037"},
    "les": {"bg": "#2B4A33", "fg": "#D5C496", "logs": "#D5C496", "btn_text": "white"},
    "myata": {"bg": "#DDFFEB", "fg": "#51705E", "logs": "#A4D4AD", "btn_text": "white"},
    "vino": {"bg": "#590507", "fg": "#FFDCDC", "logs": "#CA6F6F", "btn_text": "white"},
    "sakura": {"bg": "#FFDDE8", "fg": "#6D3068", "logs": "#FDA6BC", "btn_text": "white"},
    "bezdna": {"bg": "#223566", "fg": "white", "logs": "#CCF5EE", "btn_text": "white"},
    "oblako": {"bg": "#C7F0FF", "fg": "#1D3557", "logs": "#52A5C3", "btn_text": "white"},
    "ametist": {"bg": "#45325D", "fg": "white", "logs": "#EEE4F5", "btn_text": "white"},
    "lavanda": {"bg": "#F6D4FF", "fg": "#4A306D", "logs": "#C0A2C4", "btn_text": "white"},
    "shokolad": {"bg": "#371C18", "fg": "white", "logs": "#CDAB8A", "btn_text": "white"},
    "latte": {"bg": "#F3DFD3", "fg": "#603808", "logs": "#D5A996", "btn_text": "white"},
}

LANGUAGES = {
    "RU": {
        "start": "НАЧАТЬ",
        "status_wait": "ОЖИДАНИЕ...",
        "status_proc": "ПРОЦЕСС...",
        "status_done": "ЗАВЕРШЕНО!",
        "no_folder": "Папка не выбрана",
        "other": "Другое",
        "foolder": "Папка: ",
        "log_start": "🚀 Начинаю сортировку в: ",
        "done_msg": "Сортировка завершена!\nФайлов: ",
        "pls_folder" : "Пожалуйста, перетащите ПАПКУ, а не отдельный файл",
        "crit_err": "🚨 Критическая ошибка: ",
        "file_err": "❌ Ошибка файла {file}: ",
        "easter_text": "StarSync by GalLogicx\nВерсия 1.0\nСоздано с <3\n© 2026, GalLogicx Soft",
        "folders": {
            "Images": "Изображения",
            "Docs": "Документы",
            "Music": "Музыка",
            "Video": "Видео",
            "Mods": "Моды",
            "Archives": "Архивы",
            "Apps": "Приложения",
            "Code": "Код",
            "Design": "Дизайн" 
        },   
        "settings": {
            "settings_what": "Сортировать",
            "settings_how": "Сортировать как...",
            "settings_themes": "Темы",
            "all": "Всё",
            "mode_std": "Обычная",
            "mode_day": "По дням",
            "mode_month": "По месяцам",
            "mode_year": "По годам"
        }
    },
    "EN": {
        "start": "START",
        "status_wait": "WAITING...",
        "status_proc": "PROCESSING...",
        "status_done": "DONE!",
        "no_folder": "Folder not selected",
        "other": "Others",
        "foolder": "Folder: ",
        "easter_text": "StarSync by GalLogicx\nVersion 1.0\nCreated with <3\n© 2026, GalLogicx Soft",
        "log_start": "🚀 Starting sorting in: ",
        "done_msg": "Sorting finished!\nFiles: ",
        "pls_folder" : "Please drag and drop the FOLDER, not an individual file",
        "crit_err": "🚨 Critical error: ",
        "file_err": "❌ Error with file {file}: ",
        "folders": {
            "Images": "Images",
            "Docs": "Documents",
            "Music": "Music",
            "Mods": "Mods",
            "Video": "Video",
            "Archives": "Archives",
            "Apps": "Apps",
            "Code": "Code",
            "Design": "Design"
        },
         "settings": {
            "settings_what": "Sort Categories",
            "settings_how": "Sort Mode",
            "settings_themes": "Themes",
            "all": "All",
            "mode_std": "Standard",
            "mode_day": "By Days",
            "mode_month": "By Months",
            "mode_year": "By Years"
        }
    },
    "ZH": { # Китайский
        "start": "开始",
        "status_wait": "等待中...",
        "status_proc": "处理中...",
        "status_done": "完成！",
        "no_folder": "未選擇文件夾",
        "other": "其他",
        "foolder": "文件夹: ",
        "pls_folder" : "请拖放整个文件夹，而不是单个文件",
        "log_start": "🚀 開始排序：",
        "easter_text": "StarSync by GalLogicx\n版本 1.0\n用 <3 创作\n© 2026, GalLogicx Soft",
        "done_msg": "排序完成！\n文件： ",
        "crit_err": "🚨 严重错误: ",
        "file_err": "❌ 文件错误 {file}: ",
        "settings": {
            "settings_what": "分类",
            "settings_how": "排序方式...",
            "settings_themes": "主题",
            "all": "全部",
            "mode_std": "默认",
            "mode_day": "按天",
            "mode_month": "按月",
            "mode_year": "按年",
        },
        "folders": {
            "Images": "图片",
            "Docs": "文档",
            "Music": "音乐",
            "Mods": "模组",
            "Video": "视频",
            "Archives": "压缩包",
            "Apps": "应用",
            "Code": "代码",
            "Design": "设计"
        }
    },
    "ES": { # Испанский
        "start": "EMPEZAR",
        "status_wait": "ESPERA...",
        "status_proc": "PROCESANDO...",
        "status_done": "¡LISTO!",
        "no_folder": "Carpeta no seleccionada",
        "other": "Otros",
        "foolder": "Carpeta: ",
        "easter_text": "StarSync by GalLogicx\nVersión 1.0\nCreado con <3\n© 2026, GalLogicx Soft",
        "pls_folder" : "Por favor, arrastra la CARPETA, не un archivo individual",
        "log_start": "🚀 Iniciando en: ",
        "done_msg": "¡Orden completado!\nArchivos: ",
        "crit_err": "🚨 Error crítico: ",
        "file_err": "❌ Error con el archivo {file}: ",
        "settings": {
            "settings_what": "Clasificar",
            "settings_how": "Ordenar por...",
            "settings_themes": "Temas",
            "all": "Todo",
            "mode_std": "Normal",
            "mode_day": "Por días",
            "mode_month": "Por meses",
            "mode_year": "Por años",
        },
        "folders": {
            "Images": "Imágenes",
            "Docs": "Documentos",
            "Music": "Música",
            "Video": "Videos",
            "Mods": "Mods",
            "Archives": "Archivos",
            "Apps": "Aplicaciones",
            "Code": "Código",
            "Design": "Diseño"
        }
    }
}

formats = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".tif", ".tiff", ".ico", ".raw", ".heic"],
            "Docs": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".rtf", ".csv", ".epub", ".fb2"],
            "Music": [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".mid", ".midi"],
            "Video": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".3gp", ".webm", ".mpeg", ".mpg"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".bz2", ".xz", ".zst"],
            "Apps": [".exe", ".msi", ".apk", ".bat", ".com", ".cmd", ".scr"],
            "Mods": [
                    ".jar", ".pak", ".mod", ".package", ".ts4script", ".mcaddon", ".mcpack", ".unitypackage", 
                    ".esp", ".esm", ".ba2", ".vpk", ".pk3", ".pk4"
            ],
            "Code": [".py", ".js", ".html", ".css", ".cpp", ".c", ".cs", ".json", ".sql", ".db", ".sqlite", ".xml", ".php", ".sh"],
            "Design": [".psd", ".ai", ".fig", ".sketch", ".xd", ".blend", ".max", ".3ds", ".stl", ".obj"]
        }