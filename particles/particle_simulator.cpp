#include <SFML/Graphics.hpp>
#include <iostream>
#include <cmath>
#include <random>

using namespace std;

// Gravity constant
int G = 10;
float maxForce = 0.2;
float friction = 0.00001;


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
        if (0 > x || x > 800) {vx = -vx;}
        if (0 > y || y > 600) {vy = -vy;}
        circle.setPosition(x, y);
    }

    void updateSpeed(float dt, std::vector<Particle>* particles){
        if (particles != nullptr){
            for (Particle& p : *particles) {
                // Below control the attraction/repellion of the particle
                float attraction = (p.p_type == p_type == 1) ? -0.5 : 1.0;
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
                vx = (vx + tot_vx) * (1-friction);
                vy = (vy + tot_vy) * (1-friction);

            }
            
        }
    }
};


void updateSpeed(){

}

int generateRandomNumber(int min, int max) {
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_int_distribution<int> distribution(min, max);
    return distribution(generator);
}


int main() {

    // create the particles
    std::vector<Particle> particles = {};
    particles.emplace_back(200, 200, 5, 0, 0, 1, 0);
    particles.emplace_back(400, 200, 0, 5, 0, 1, 0);
    particles.emplace_back(200, 400, 0, -5, 0, 1, 0);
    particles.emplace_back(400, 400, -5, 0, 0, 1, 0);

    
    for(int i = 0; i < 200; i++){
        particles.emplace_back(generateRandomNumber(0, 800), generateRandomNumber(0, 600), 0, 0, 0, 1, 0);
    }

    for(int i = 0; i < 200; i++){
        particles.emplace_back(generateRandomNumber(0, 800), generateRandomNumber(0, 600), 0, 0, 1, 1, 0);
    }

    sf::RenderWindow window(sf::VideoMode(800, 600), "Particles");
    sf::Clock clock;
    sf:: Time accumulator = sf::Time::Zero;
    sf::Time timestep = sf::seconds(1.0f / 60.0f);

    std::map<int, sf::Color> colorDict;
    colorDict[0] = sf::Color::Red;
    colorDict[1] = sf::Color::Green;
    colorDict[2] = sf::Color::Blue;    

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
                particle.updateSpeed(1, &particles);
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
