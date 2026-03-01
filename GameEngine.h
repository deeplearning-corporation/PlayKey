// GameEngine.h
#pragma once

#ifdef GAMEENGINE_EXPORTS
#define GAMEENGINE_API __declspec(dllexport)
#else
#define GAMEENGINE_API __declspec(dllimport)
#endif

#include <string>
#include <vector>

class GAMEENGINE_API GameEngine {
public:
    GameEngine();
    ~GameEngine();

    // 初始化引擎
    bool Initialize(int width, int height);

    // 物理引擎
    void UpdatePhysics(float deltaTime);
    bool CheckCollision(float x1, float y1, float r1, float x2, float y2, float r2);

    // 粒子效果
    void CreateParticleEffect(float x, float y, int type);
    void UpdateParticles(float deltaTime);

    // 渲染
    void Render();

    // 游戏状态
    void SetGameState(int state);
    int GetGameState();

private:
    void* m_renderer;
    void* m_physicsWorld;
    std::vector<void*> m_particles;
    int m_gameState;
};