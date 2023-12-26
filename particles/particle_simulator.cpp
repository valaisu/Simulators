#include <SFML/Graphics.hpp>
#include <iostream>
#include <cmath>
#include <random>

using namespace std;

// Gravity constant
int G = 200;
float maxForce = 0.3;
float maxSpeed = 10.0;
float friction = 0.002;
int size_x = 900;
int size_y = 900;


class Particle {
public:
    float x, y, vx, vy;
    int p_type;
    float mass;
    float charge;
    sf::CircleShape circle = sf::CircleShape(3);

    Particle(float x, float y, float vx, float vy, int p_type, float mass, float charge) 
    : x(x), y(y), vx(vx), vy(vy), p_type(p_type), mass(mass), charge(charge) {}

    void updatePosition(float dt){
        x += vx * dt;
        y += vy * dt;
        if (50 > x || x > size_x-50) {vx = -vx;}
        if (50 > y || y > size_y-50) {vy = -vy;}
        circle.setPosition(x, y);
    }

    void updateSpeed(float dt, std::vector<Particle>* particles, std::map<std::pair<int, int>, float>* table){
        if (particles != nullptr){
            for (Particle& p : *particles) {
                // Below control the attraction/repellion of the particle
                float attraction = (*table)[{p_type, p.p_type}];
                float dx = p.x - x, dy = p.y - y;
                float tot_vx = 0, tot_vy = 0;
                if (dx != 0 || dy != 0) {
                    float r2 = dx*dx + dy*dy;
                    // too high forces break the simulation, 
                    // in reality particles can't get too close to each other
                    float f = std::min((p.mass * mass) * G / r2, maxForce) * attraction;
                    float fx = f * dx / (abs(dx) + abs(dy));
                    float fy = f * dy / (abs(dx) + abs(dy));
                    tot_vx += (fx / mass * dt);
                    tot_vy += (fy / mass * dt);
                }
                vx = std::min((vx + tot_vx) * (1-friction), maxSpeed);
                vy = std::min((vy + tot_vy) * (1-friction), maxSpeed);

            }
            
        }
    }
};



int generateRandomNumber(int min, int max) {
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_int_distribution<int> distribution(min, max);
    return distribution(generator);
}


float grf(float min, float max) {
    static std::mt19937 engine(std::random_device{}());
    std::uniform_real_distribution<float> distribution(min, max);
    return distribution(engine);
}


int main() {

    // create the particles
    std::vector<Particle> particles = {};
    particles.emplace_back(400, 400, 5, 0, 0, 1, 0);
    particles.emplace_back(600, 400, 0, 5, 0, 1, 0);
    particles.emplace_back(400, 600, 0, -5, 0, 1, 0);
    particles.emplace_back(600, 600, -5, 0, 0, 1, 0);

    
    for(int i = 0; i < 100; i++){
        particles.emplace_back(generateRandomNumber(0, size_x), generateRandomNumber(0, size_y), 0, 0, 0, 1, 0);
    }

    for(int i = 0; i < 100; i++){
        particles.emplace_back(generateRandomNumber(0, size_x), generateRandomNumber(0, size_y), 0, 0, 1, 1, 0);
    }

    for(int i = 0; i < 100; i++){
        particles.emplace_back(generateRandomNumber(0, size_x), generateRandomNumber(0, size_y), 0, 0, 2, 1, 0);
    }

    sf::RenderWindow window(sf::VideoMode(size_x, size_y), "Particles");
    sf::Clock clock;
    sf:: Time accumulator = sf::Time::Zero;
    sf::Time timestep = sf::seconds(1.0f / 60.0f);

    std::map<int, sf::Color> colorDict;
    colorDict[0] = sf::Color::Red;
    colorDict[1] = sf::Color::Green;
    colorDict[2] = sf::Color::Blue;

    std::map<std::pair<int, int>, float> attractionDict;

    float min = -4.0f, max = 4.0f;


    /*
    //SYMMETRIC
    //std::vector<float> rfloats = {grf(min, max), grf(min, max), grf(min, max), grf(min, max), grf(min, max), grf(min, max)};
    //                                1              2, 4           3, 7           5              6,  8           9
    std::vector<float> rfloats = {2, 3, -6, 2, -1.5, 0};
    //                            1  24  37 5  68   9
    std::cout << rfloats[0]<<" "<<rfloats[1]<<" "<<rfloats[2]<< std::endl;
    std::cout << rfloats[1]<<" "<<rfloats[3]<<" "<<rfloats[4]<<std::endl;
    std::cout << rfloats[2]<<" "<<rfloats[4]<<" "<<rfloats[5]<<std::endl;

    attractionDict[{0, 0}] = rfloats[0];
    attractionDict[{0, 1}] = rfloats[1];
    attractionDict[{0, 2}] = rfloats[2];

    attractionDict[{1, 0}] = rfloats[1];
    attractionDict[{1, 1}] = rfloats[3];
    attractionDict[{1, 2}] = rfloats[4];

    attractionDict[{2, 0}] = rfloats[2];
    attractionDict[{2, 1}] = rfloats[4];
    attractionDict[{2, 2}] = rfloats[5];
    */



    std::vector<float> rfloats = {grf(min, max), grf(min, max), grf(min, max), grf(min, max), grf(min, max), grf(min, max), grf(min, max), grf(min, max), grf(min, max)};
    std::cout << rfloats[0]<<" "<<rfloats[1]<<" "<<rfloats[2]<< std::endl;
    std::cout << rfloats[3]<<" "<<rfloats[4]<<" "<<rfloats[5]<<std::endl;
    std::cout << rfloats[6]<<" "<<rfloats[7]<<" "<<rfloats[8]<<std::endl;

    attractionDict[{0, 0}] = rfloats[0];
    attractionDict[{0, 1}] = rfloats[1];
    attractionDict[{0, 2}] = rfloats[2];

    attractionDict[{1, 0}] = rfloats[3];
    attractionDict[{1, 1}] = rfloats[4];
    attractionDict[{1, 2}] = rfloats[5];

    attractionDict[{2, 0}] = rfloats[6];
    attractionDict[{2, 1}] = rfloats[7];
    attractionDict[{2, 2}] = rfloats[8];





    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        sf::Time elapsed = clock.restart();
        accumulator += elapsed;

        // Update at fixed timesteps
        while (accumulator >= timestep) {
            accumulator -= timestep;

            window.clear();
            for (auto& particle : particles) {
                particle.updateSpeed(1, &particles, &attractionDict);
            }
            for (auto& particle : particles) {
                particle.updatePosition(1);
                particle.circle.setFillColor(colorDict[particle.p_type]);
                window.draw(particle.circle);
            }

            window.display();
        }
    }

    return 0;
}
