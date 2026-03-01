// AudioSystem.cpp
#include "AudioSystem.h"
#include <iostream>

AudioSystem::AudioSystem() : m_masterVolume(1.0f), m_musicVolume(1.0f), m_sfxVolume(1.0f), m_currentMusic(nullptr) {
    std::cout << "AudioSystem 初始化..." << std::endl;
}

AudioSystem::~AudioSystem() {
    std::cout << "AudioSystem 清理..." << std::endl;
}

bool AudioSystem::Initialize(int sampleRate, int channels) {
    std::cout << "初始化音频系统: " << sampleRate << "Hz, " << channels << "声道" << std::endl;
    return true;
}

int AudioSystem::LoadSound(const char* filename) {
    static int nextId = 1000;
    int id = nextId++;
    std::cout << "加载音效: " << filename << " (ID: " << id << ")" << std::endl;
    m_sounds[id] = (void*)id;
    return id;
}

int AudioSystem::LoadMusic(const char* filename) {
    static int nextId = 2000;
    int id = nextId++;
    std::cout << "加载音乐: " << filename << " (ID: " << id << ")" << std::endl;
    m_music[id] = (void*)id;
    return id;
}

void AudioSystem::PlaySound(int soundId, float volume, float pan) {
    if (m_sounds.find(soundId) != m_sounds.end()) {
        std::cout << "播放音效 ID: " << soundId << ", 音量: " << volume << ", 声道: " << pan << std::endl;
    }
}

void AudioSystem::PlayMusic(int musicId, bool loop) {
    if (m_music.find(musicId) != m_music.end()) {
        m_currentMusic = m_music[musicId];
        std::cout << "播放音乐 ID: " << musicId << ", 循环: " << (loop ? "是" : "否") << std::endl;
    }
}

void AudioSystem::StopMusic() {
    std::cout << "停止音乐" << std::endl;
    m_currentMusic = nullptr;
}

void AudioSystem::PauseMusic() {
    std::cout << "暂停音乐" << std::endl;
}

void AudioSystem::ResumeMusic() {
    std::cout << "恢复音乐" << std::endl;
}

void AudioSystem::SetListenerPosition(float x, float y, float z) {
    std::cout << "设置听者位置: (" << x << ", " << y << ", " << z << ")" << std::endl;
}

void AudioSystem::SetSoundPosition(int soundId, float x, float y, float z) {
    if (m_sounds.find(soundId) != m_sounds.end()) {
        std::cout << "设置音效 " << soundId << " 位置: (" << x << ", " << y << ", " << z << ")" << std::endl;
    }
}

void AudioSystem::SetMasterVolume(float volume) {
    m_masterVolume = volume;
    std::cout << "设置主音量: " << volume << std::endl;
}

void AudioSystem::SetMusicVolume(float volume) {
    m_musicVolume = volume;
    std::cout << "设置音乐音量: " << volume << std::endl;
}

void AudioSystem::SetSFXVolume(float volume) {
    m_sfxVolume = volume;
    std::cout << "设置音效音量: " << volume << std::endl;
}