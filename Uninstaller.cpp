// Uninstaller.cpp
#include <windows.h>
#include <shlobj.h>
#include <tlhelp32.h>  // 添加这个头文件用于进程快照
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <direct.h>
#include <stdio.h>

#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "user32.lib")
#pragma comment(lib, "advapi32.lib")

// 颜色定义
#define COLOR_RESET 7
#define COLOR_RED 12
#define COLOR_GREEN 10
#define COLOR_YELLOW 14
#define COLOR_CYAN 11
#define COLOR_WHITE 15

class Uninstaller {
private:
    std::wstring installPath;
    std::wstring uninstallPath;
    std::vector<std::wstring> filesToRemove;
    std::vector<std::wstring> dirsToRemove;
    bool isSilent;

    void SetConsoleColor(int color) {
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color);
    }

    void PrintMessage(const std::wstring& msg, int color = COLOR_RESET) {
        if (!isSilent) {
            SetConsoleColor(color);
            std::wcout << msg << std::endl;
            SetConsoleColor(COLOR_RESET);
        }
    }

    bool DirectoryExists(const std::wstring& path) {
        DWORD attrib = GetFileAttributesW(path.c_str());
        return (attrib != INVALID_FILE_ATTRIBUTES && (attrib & FILE_ATTRIBUTE_DIRECTORY));
    }

    bool FileExists(const std::wstring& path) {
        DWORD attrib = GetFileAttributesW(path.c_str());
        return (attrib != INVALID_FILE_ATTRIBUTES && !(attrib & FILE_ATTRIBUTE_DIRECTORY));
    }

    void FindInstallPath() {
        wchar_t modulePath[MAX_PATH];
        GetModuleFileNameW(NULL, modulePath, MAX_PATH);

        // 获取卸载程序所在路径
        std::wstring exePath(modulePath);
        size_t lastSlash = exePath.find_last_of(L"\\");
        if (lastSlash != std::wstring::npos) {
            installPath = exePath.substr(0, lastSlash);
            uninstallPath = exePath;
        }

        PrintMessage(L"安装目录: " + installPath, COLOR_CYAN);
    }

    void CollectFiles() {
        // 添加要删除的文件
        std::vector<std::wstring> extensions = {
            L"*.exe", L"*.dll", L"*.pyd", L"*.pyc", L"*.pyo",
            L"*.json", L"*.txt", L"*.log", L"*.dat", L"*.cfg",
            L"*.wav", L"*.mp3", L"*.ogg", L"*.png", L"*.jpg",
            L"*.ico", L"*.svg", L"*.ttf", L"*.spec"
        };

        WIN32_FIND_DATAW findData;
        HANDLE hFind;

        for (const auto& ext : extensions) {
            std::wstring searchPath = installPath + L"\\" + ext;
            hFind = FindFirstFileW(searchPath.c_str(), &findData);

            if (hFind != INVALID_HANDLE_VALUE) {
                do {
                    if (!(findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
                        std::wstring filePath = installPath + L"\\" + findData.cFileName;
                        filesToRemove.push_back(filePath);
                    }
                } while (FindNextFileW(hFind, &findData) != 0);
                FindClose(hFind);
            }
        }

        // 添加子目录
        std::vector<std::wstring> subDirs = {
            L"__pycache__", L"build", L"dist", L"output",
            L"logs", L"data", L"temp", L"cache", L"fonts"
        };

        for (const auto& dir : subDirs) {
            std::wstring dirPath = installPath + L"\\" + dir;
            if (DirectoryExists(dirPath)) {
                dirsToRemove.push_back(dirPath);
            }
        }
    }

    bool KillProcesses() {
        PrintMessage(L"正在关闭PlayKey相关进程...", COLOR_YELLOW);

        HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (hSnapshot == INVALID_HANDLE_VALUE) return false;

        PROCESSENTRY32W pe;
        pe.dwSize = sizeof(PROCESSENTRY32W);

        if (Process32FirstW(hSnapshot, &pe)) {
            do {
                std::wstring processName = pe.szExeFile;
                if (processName.find(L"PlayKey") != std::wstring::npos ||
                    processName.find(L"python") != std::wstring::npos) {

                    HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, pe.th32ProcessID);
                    if (hProcess) {
                        TerminateProcess(hProcess, 0);
                        CloseHandle(hProcess);
                        PrintMessage(L"  已终止: " + processName, COLOR_RED);
                    }
                }
            } while (Process32NextW(hSnapshot, &pe));
        }

        CloseHandle(hSnapshot);
        return true;
    }

    bool RemoveFiles() {
        PrintMessage(L"正在删除文件...", COLOR_YELLOW);

        // 先删除只读属性
        for (const auto& file : filesToRemove) {
            SetFileAttributesW(file.c_str(), FILE_ATTRIBUTE_NORMAL);
        }

        // 删除文件
        int successCount = 0;
        for (const auto& file : filesToRemove) {
            if (DeleteFileW(file.c_str())) {
                successCount++;
                if (!isSilent) {
                    std::wcout << L"  ✓ 已删除: " << file.substr(installPath.length() + 1) << std::endl;
                }
            }
        }

        PrintMessage(L"已删除 " + std::to_wstring(successCount) + L" 个文件", COLOR_GREEN);
        return true;
    }

    bool RemoveDirectories() {
        PrintMessage(L"正在删除目录...", COLOR_YELLOW);

        int successCount = 0;
        for (const auto& dir : dirsToRemove) {
            // 使用递归删除
            SHFILEOPSTRUCTW fileOp = { 0 };
            std::wstring from = dir + L"\0\0";
            fileOp.wFunc = FO_DELETE;
            fileOp.pFrom = from.c_str();
            fileOp.fFlags = FOF_NO_UI | FOF_SILENT | FOF_NOCONFIRMATION;

            if (SHFileOperationW(&fileOp) == 0) {
                successCount++;
                if (!isSilent) {
                    std::wcout << L"  ✓ 已删除目录: " << dir.substr(installPath.length() + 1) << std::endl;
                }
            }
        }

        PrintMessage(L"已删除 " + std::to_wstring(successCount) + L" 个目录", COLOR_GREEN);
        return true;
    }

    bool RemoveShortcuts() {
        PrintMessage(L"正在删除快捷方式...", COLOR_YELLOW);

        // 获取桌面路径
        wchar_t desktopPath[MAX_PATH];
        SHGetSpecialFolderPathW(NULL, desktopPath, CSIDL_DESKTOP, FALSE);

        // 获取开始菜单路径
        wchar_t startMenuPath[MAX_PATH];
        SHGetSpecialFolderPathW(NULL, startMenuPath, CSIDL_PROGRAMS, FALSE);

        std::vector<std::wstring> shortcutPaths = {
            std::wstring(desktopPath) + L"\\PlayKey.lnk",
            std::wstring(startMenuPath) + L"\\PlayKey\\PlayKey.lnk",
            std::wstring(startMenuPath) + L"\\PlayKey\\Uninstall PlayKey.lnk"
        };

        for (const auto& shortcut : shortcutPaths) {
            if (DeleteFileW(shortcut.c_str())) {
                PrintMessage(L"  ✓ 已删除快捷方式: " + shortcut, COLOR_GREEN);
            }
        }

        // 删除开始菜单文件夹
        std::wstring startMenuDir = std::wstring(startMenuPath) + L"\\PlayKey";
        if (DirectoryExists(startMenuDir)) {
            RemoveDirectoryW(startMenuDir.c_str());
        }

        return true;
    }

    bool CleanRegistry() {
        PrintMessage(L"正在清理注册表...", COLOR_YELLOW);

        HKEY hKey;
        std::wstring regPath = L"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\PlayKey";

        if (RegOpenKeyExW(HKEY_CURRENT_USER, regPath.c_str(), 0, KEY_ALL_ACCESS, &hKey) == ERROR_SUCCESS) {
            // 删除所有子键
            RegDeleteTreeW(hKey, NULL);
            RegCloseKey(hKey);
            RegDeleteKeyW(HKEY_CURRENT_USER, regPath.c_str());
            PrintMessage(L"  ✓ 已删除注册表项", COLOR_GREEN);
        }

        return true;
    }

    void ShowSummary() {
        if (isSilent) return;

        PrintMessage(L"\n═══════════════════════════════════════", COLOR_CYAN);
        PrintMessage(L"          卸载完成", COLOR_GREEN);
        PrintMessage(L"═══════════════════════════════════════", COLOR_CYAN);
        PrintMessage(L"已删除:", COLOR_YELLOW);
        PrintMessage(L"  • " + std::to_wstring(filesToRemove.size()) + L" 个文件", COLOR_WHITE);
        PrintMessage(L"  • " + std::to_wstring(dirsToRemove.size()) + L" 个目录", COLOR_WHITE);
        PrintMessage(L"  • 所有快捷方式", COLOR_WHITE);
        PrintMessage(L"  • 注册表项", COLOR_WHITE);
        PrintMessage(L"\nPlayKey 已成功从您的计算机中移除", COLOR_GREEN);
        PrintMessage(L"═══════════════════════════════════════\n", COLOR_CYAN);
    }

    void ShowConfirmationDialog() {
        if (isSilent) return;

        std::wstring message = L"确定要卸载 PlayKey 吗？\n\n";
        message += L"安装目录: " + installPath + L"\n";
        message += L"将删除 " + std::to_wstring(filesToRemove.size()) + L" 个文件和 ";
        message += std::to_wstring(dirsToRemove.size()) + L" 个目录。";

        int result = MessageBoxW(NULL, message.c_str(), L"卸载 PlayKey",
            MB_YESNO | MB_ICONQUESTION | MB_DEFBUTTON2);

        if (result != IDYES) {
            PrintMessage(L"卸载已取消", COLOR_YELLOW);
            exit(0);
        }
    }

public:
    Uninstaller() : isSilent(false) {
        FindInstallPath();
    }

    void ParseArguments(int argc, char* argv[]) {
        for (int i = 1; i < argc; i++) {
            std::string arg = argv[i];
            if (arg == "/S" || arg == "-silent" || arg == "/silent") {
                isSilent = true;
            }
        }
    }

    bool Execute() {
        PrintMessage(L"\n═══════════════════════════════════════", COLOR_CYAN);
        PrintMessage(L"      PlayKey 卸载程序", COLOR_GREEN);
        PrintMessage(L"═══════════════════════════════════════\n", COLOR_CYAN);

        // 检查安装目录
        if (!DirectoryExists(installPath)) {
            PrintMessage(L"错误: 找不到安装目录!", COLOR_RED);
            return false;
        }

        // 收集要删除的文件
        CollectFiles();

        // 显示确认对话框
        ShowConfirmationDialog();

        // 执行卸载
        bool success = true;

        // 1. 关闭进程
        if (!KillProcesses()) {
            PrintMessage(L"警告: 无法关闭所有进程", COLOR_YELLOW);
        }

        // 2. 删除文件
        if (!RemoveFiles()) {
            success = false;
        }

        // 3. 删除目录
        if (!RemoveDirectories()) {
            success = false;
        }

        // 4. 删除快捷方式
        RemoveShortcuts();

        // 5. 清理注册表
        CleanRegistry();

        // 6. 删除自身（需要创建批处理文件）
        if (success) {
            DeleteSelf();
        }

        // 显示总结
        ShowSummary();

        if (!isSilent) {
            MessageBoxW(NULL, L"PlayKey 已成功卸载！", L"卸载完成", MB_OK | MB_ICONINFORMATION);
        }

        return success;
    }

    void DeleteSelf() {
        // 创建批处理文件来删除自身
        std::wstring batPath = installPath + L"\\del_temp.bat";
        std::wofstream batFile(batPath);

        batFile << L"@echo off\n";
        batFile << L"timeout /t 2 /nobreak >nul\n";
        batFile << L":loop\n";
        batFile << L"del /f /q \"" << uninstallPath << L"\"\n";
        batFile << L"if exist \"" << uninstallPath << L"\" goto loop\n";
        batFile << L"del /f /q \"" << batPath << L"\"\n";
        batFile.close();

        // 执行批处理文件
        ShellExecuteW(NULL, L"open", batPath.c_str(), NULL, NULL, SW_HIDE);
    }
};

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // 检查是否以管理员权限运行
    BOOL isAdmin = FALSE;
    PSID adminGroup = NULL;
    SID_IDENTIFIER_AUTHORITY ntAuthority = SECURITY_NT_AUTHORITY;

    if (AllocateAndInitializeSid(&ntAuthority, 2, SECURITY_BUILTIN_DOMAIN_RID,
        DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, &adminGroup)) {
        CheckTokenMembership(NULL, adminGroup, &isAdmin);
        FreeSid(adminGroup);
    }

    if (!isAdmin) {
        // 请求管理员权限
        wchar_t exePath[MAX_PATH];
        GetModuleFileNameW(NULL, exePath, MAX_PATH);

        SHELLEXECUTEINFOW sei = { sizeof(sei) };
        sei.lpVerb = L"runas";
        sei.lpFile = exePath;
        sei.lpParameters = L"";
        sei.hwnd = NULL;
        sei.nShow = SW_NORMAL;

        if (!ShellExecuteExW(&sei)) {
            MessageBoxW(NULL, L"需要管理员权限才能卸载程序", L"权限不足", MB_OK | MB_ICONERROR);
            return 1;
        }
        return 0;
    }

    // 解析命令行参数
    int argc = __argc;
    char** argv = __argv;

    // 创建卸载程序实例
    Uninstaller uninstaller;
    uninstaller.ParseArguments(argc, argv);

    // 执行卸载
    if (uninstaller.Execute()) {
        return 0;
    }
    else {
        MessageBoxW(NULL, L"卸载过程中出现错误", L"错误", MB_OK | MB_ICONERROR);
        return 1;
    }
}