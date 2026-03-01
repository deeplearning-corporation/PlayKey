// AudioSystem.h
#pragma once

#ifdef AUDIOSYSTEM_EXPORTS
#define AUDIOSYSTEM_API __declspec(dllexport)
#else
#define AUDIOSYSTEM_API __declspec(dllimport)
#endif

#include <string>
#include <map>

class AUDIOSYSTEM_API AudioSystem {
public:
    AudioSystem();
    ~AudioSystem();

    // 初始化音频系统
    bool Initialize(int sampleRate, int channels);

    // 加载音效
    int LoadSound(const char* filename);
    int LoadMusic(const char* filename);

    // 播放控制
    void PlaySound(int soundId, float volume, float pan);
    void PlayMusic(int musicId, bool loop);
    void StopMusic();
    void PauseMusic();
    void ResumeMusic();

    // 3D音频
    void SetListenerPosition(float x, float y, float z);
    void SetSoundPosition(int soundId, float x, float y, float z);

    // 音量控制
    void SetMasterVolume(float volume);
    void SetMusicVolume(float volume);
    void SetSFXVolume(float volume);

private:
    std::map<int, void*> m_sounds;
    std::map<int, void*> m_music;
    float m_masterVolume;
    float m_musicVolume;
    float m_sfxVolume;
    void* m_currentMusic;
};