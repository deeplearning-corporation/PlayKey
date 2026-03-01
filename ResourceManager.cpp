// ResourceManager.cpp
#include "ResourceManager.h"
#include <iostream>
#include <fstream>
#include <sstream>

ResourceManager::ResourceManager() : m_maxCacheSize(1024 * 1024 * 256), m_currentCacheSize(0) {
    std::cout << "ResourceManager 初始化..." << std::endl;
}

ResourceManager::~ResourceManager() {
    ClearCache();
    std::cout << "ResourceManager 清理..." << std::endl;
}

bool ResourceManager::Initialize(const char* resourcePath) {
    m_resourcePath = resourcePath;
    std::cout << "设置资源路径: " << resourcePath << std::endl;
    return true;
}

int ResourceManager::LoadTexture(const char* filename) {
    static int nextId = 1;
    int id = nextId++;
    std::cout << "加载纹理: " << filename << " (ID: " << id << ")" << std::endl;
    m_textures[id] = (void*)id;
    m_currentCacheSize += 1024 * 1024; // 模拟1MB
    return id;
}

void* ResourceManager::GetTexture(int textureId) {
    if (m_textures.find(textureId) != m_textures.end()) {
        return m_textures[textureId];
    }
    return nullptr;
}

void ResourceManager::UnloadTexture(int textureId) {
    if (m_textures.find(textureId) != m_textures.end()) {
        std::cout << "卸载纹理 ID: " << textureId << std::endl;
        m_textures.erase(textureId);
        m_currentCacheSize -= 1024 * 1024;
    }
}

int ResourceManager::LoadModel(const char* filename) {
    static int nextId = 1000;
    int id = nextId++;
    std::cout << "加载模型: " << filename << " (ID: " << id << ")" << std::endl;
    m_models[id] = (void*)id;
    m_currentCacheSize += 5 * 1024 * 1024; // 模拟5MB
    return id;
}

void* ResourceManager::GetModel(int modelId) {
    if (m_models.find(modelId) != m_models.end()) {
        return m_models[modelId];
    }
    return nullptr;
}

int ResourceManager::LoadAudioClip(const char* filename) {
    static int nextId = 2000;
    int id = nextId++;
    std::cout << "加载音频: " << filename << " (ID: " << id << ")" << std::endl;
    m_audioClips[id] = (void*)id;
    m_currentCacheSize += 512 * 1024; // 模拟512KB
    return id;
}

void* ResourceManager::GetAudioClip(int clipId) {
    if (m_audioClips.find(clipId) != m_audioClips.end()) {
        return m_audioClips[clipId];
    }
    return nullptr;
}

bool ResourceManager::LoadConfig(const char* filename) {
    std::cout << "加载配置文件: " << filename << std::endl;

    // 模拟配置数据
    m_config["version"] = "1.0.0";
    m_config["max_players"] = "10";
    m_config["game_duration"] = "60";
    m_config["default_volume"] = "0.8";
    m_config["language"] = "zh_CN";

    return true;
}

std::string ResourceManager::GetConfigValue(const char* key) {
    if (m_config.find(key) != m_config.end()) {
        return m_config[key];
    }
    return "";
}

void ResourceManager::ClearCache() {
    std::cout << "清理缓存，释放 " << m_currentCacheSize / (1024 * 1024) << "MB 内存" << std::endl;
    m_textures.clear();
    m_models.clear();
    m_audioClips.clear();
    m_currentCacheSize = 0;
}

void ResourceManager::SetMaxCacheSize(size_t maxSize) {
    m_maxCacheSize = maxSize;
    std::cout << "设置最大缓存: " << maxSize / (1024 * 1024) << "MB" << std::endl;
}