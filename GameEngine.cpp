// GameEngine.cpp
#include "GameEngine.h"
#include <cmath>
#include <iostream>

GameEngine::GameEngine() : m_renderer(nullptr), m_physicsWorld(nullptr), m_gameState(0) {
    std::cout << "GameEngine 初始化..." << std::endl;
}

GameEngine::~GameEngine() {
    std::cout << "GameEngine 清理..." << std::endl;
}

bool GameEngine::Initialize(int width, int height) {
    std::cout << "初始化游戏引擎: " << width << "x" << height << std::endl;
    // 模拟初始化
    m_renderer = (void*)1;
    m_physicsWorld = (void*)1;
    return true;
}

void GameEngine::UpdatePhysics(float deltaTime) {
    // 模拟物理更新
    std::cout << "更新物理引擎: " << deltaTime << "s" << std::endl;
}

bool GameEngine::CheckCollision(float x1, float y1, float r1, float x2, float y2, float r2) {
    float dx = x1 - x2;
    float dy = y1 - y2;
    float distance = sqrt(dx * dx + dy * dy);
    return distance <= (r1 + r2);
}

void GameEngine::CreateParticleEffect(float x, float y, int type) {
    std::cout << "创建粒子效果: (" << x << "," << y << ") 类型 " << type << std::endl;
    m_particles.push_back((void*)m_particles.size());
}

void GameEngine::UpdateParticles(float deltaTime) {
    // 更新粒子
    std::cout << "更新 " << m_particles.size() << " 个粒子" << std::endl;
}

void GameEngine::Render() {
    std::cout << "渲染游戏画面" << std::endl;
}

void GameEngine::SetGameState(int state) {
    m_gameState = state;
    std::cout << "游戏状态改变为: " << state << std::endl;
}

int GameEngine::GetGameState() {
    return m_gameState;
}