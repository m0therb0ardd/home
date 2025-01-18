# Project: Symbiotic Dance Between a TurtleBot3 and a Dancer  
*Work in Progress*

## Project Idea  
This project explores the interplay between spatial awareness, the concept of home, and human-robot collaboration. The TurtleBot3 and a dancer create illuminated pathways that visually trace their movements, engaging in a creative dialogue about presence and belonging. Machine learning analyzes these light-drawn patterns, enabling dynamic responses between the robot and human. Inspired by Shannon Dowling's improvisational principles and Laban Dance Movement Analysis, this project combines robotics and performance art.

---

## Plan  
The project is structured into the following key stages:

1. **TurtleBot Setup and Basic Functionality**  
   - Ensure both TurtleBots are operational and capable of executing basic movement commands (forward, turn, stop).  
   - Develop initial prompts to facilitate movement and interaction.

2. **Orientation and Navigation**  
   - Implement north orientation using IMU and magnetometer data.  
   - Utilize LiDAR to navigate toward open spaces and avoid obstacles.

3. **Lighting Display and Interaction**  
   - Create an illuminated display using Arduino-controlled lights to visually trace the TurtleBot’s movements.  
   - Experiment with dynamic lighting patterns to enhance the artistic component of the performance.

4. **Path and Color Detection**  
   - Use a RealSense camera or OptiTrack system to detect paths and colors associated with light trails.  
   - Develop algorithms to enable the TurtleBot to follow light-based paths.

5. **Path Following and Shape Recognition**  
   - Integrate path-following behavior into the TurtleBot’s navigation system.  
   - Incorporate machine learning to train the robot for recognizing and responding to specific shapes or light patterns.

6. **Testing and Refinement**  
   - Conduct extensive testing of the system in a creative space, ensuring smooth interaction between the TurtleBot and dancer.  
   - Refine the choreography and technical setup to achieve a cohesive performance.


---

## Progress  

### Week 1: (January 6, 2025)
- Verified TurtleBot functionality for both robots (Teetle and Shredder).
- Created a GitHub repository to document project development.
- Programmed basic movement commands: forward, turn, and stop.
- Finalized the project proposal.
- Added a magnetic sensor to calculate north orientation.
- Began programming north orientation using the IMU (in progress).

### Week 2:  
- Improved north orientation functionality.
  - Filtered non-zero values in the `orient_to_north` node for better accuracy.
  - Noted that magnetometer values were inconsistent; identified the need for calibration without interference (e.g., on a non-metallic surface).
- Ordered a new magnetometer for reliable north orientation calculations.
- Prepared code for `orient_to_north` and `orient_to_home` to deploy once the magnetometer is operational.
- Started implementing and testing LiDAR-based movement towards open spaces.
- Began exploring path detection for dynamic navigation.
- Examined the [Light Painting Robot GitHub repository](https://github.com/241abhishek/Light-Painting-Robot/tree/main) for inspiration and technical insights.
