// ResourceManager.h
#pragma once

#ifdef RESOURCEMANAGER_EXPORTS
#define RESOURCEMANAGER_API __declspec(dllexport)
#else
#define RESOURCEMANAGER_API __declspec(dllimport)
#endif

#include <string>
#include <map>
#include <vector>

class RESOURCEMANAGER_API ResourceManager {
public:
    ResourceManager();
    ~ResourceManager();

    // 初始化
    bool Initialize(const char* resourcePath);

    // 纹理管理
    int LoadTexture(const char* filename);
    void* GetTexture(int textureId);
    void UnloadTexture(int textureId);

    // 模型管理
    int LoadModel(const char* filename);
    void* GetModel(int modelId);

    // 音频资源
    int LoadAudioClip(const char* filename);
    void* GetAudioClip(int clipId);

    // 配置文件
    bool LoadConfig(const char* filename);
    std::string GetConfigValue(const char* key);

    // 缓存管理
    void ClearCache();
    void SetMaxCacheSize(size_t maxSize);

private:
    std::string m_resourcePath;
    std::map<int, void*> m_textures;
    std::map<int, void*> m_models;
    std::map<int, void*> m_audioClips;
    std::map<std::string, std::string> m_config;
    size_t m_maxCacheSize;
    size_t m_currentCacheSize;
};