// NetworkModule.cpp
#include "NetworkModule.h"
#include <iostream>
#include <chrono>
#include <thread>

NetworkModule::NetworkModule() : m_socket(nullptr), m_connected(false) {
    std::cout << "NetworkModule 初始化..." << std::endl;
}

NetworkModule::~NetworkModule() {
    Disconnect();
    std::cout << "NetworkModule 清理..." << std::endl;
}

bool NetworkModule::Connect(const char* serverAddress, int port) {
    std::cout << "连接到服务器: " << serverAddress << ":" << port << std::endl;
    // 模拟连接延迟
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    m_connected = true;
    return true;
}

void NetworkModule::Disconnect() {
    if (m_connected) {
        std::cout << "断开服务器连接" << std::endl;
        m_connected = false;
    }
}

bool NetworkModule::IsConnected() {
    return m_connected;
}

bool NetworkModule::SendData(const char* data, int length) {
    if (!m_connected) return false;
    std::cout << "发送数据: " << std::string(data, length) << std::endl;
    return true;
}

void NetworkModule::SetMessageCallback(MessageCallback callback) {
    m_messageCallback = callback;
    std::cout << "设置消息回调函数" << std::endl;
}

bool NetworkModule::CreateRoom(const char* roomName, int maxPlayers) {
    std::cout << "创建房间: " << roomName << " (最大玩家: " << maxPlayers << ")" << std::endl;
    m_currentRoom = roomName;
    return true;
}

bool NetworkModule::JoinRoom(const char* roomName) {
    std::cout << "加入房间: " << roomName << std::endl;
    m_currentRoom = roomName;
    return true;
}

void NetworkModule::LeaveRoom() {
    std::cout << "离开房间: " << m_currentRoom << std::endl;
    m_currentRoom.clear();
}

void NetworkModule::UpdatePlayerData(const char* playerData) {
    std::cout << "更新玩家数据: " << playerData << std::endl;
}

void NetworkModule::RequestPlayerList() {
    std::cout << "请求玩家列表" << std::endl;
}

void NetworkModule::RequestLeaderboard() {
    std::cout << "请求排行榜" << std::endl;
}

void NetworkModule::SubmitScore(const char* playerName, int score) {
    std::cout << "提交分数: " << playerName << " - " << score << std::endl;
}