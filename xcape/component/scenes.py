


#
# def updateCameraX(self):
#     """
#     Updates the camera view in the x-axis.
#     """
#     maxCamera_x = int(WIDTH * 2 / 3)
#     minCamera_x = int(WIDTH / 3)
#
#     if self.playerOne.rect.right >= maxCamera_x:
#         diff = maxCamera_x - self.playerOne.rect.right
#         self.playerOne.rect.right = maxCamera_x
#         self.scenario.shiftWorldX(diff)
#
#     if self.playerOne.rect.left <= minCamera_x:
#         diff = minCamera_x - self.playerOne.rect.left
#         self.playerOne.rect.left = minCamera_x
#         self.scenario.shiftWorldX(diff)
#
# def updateCameraY(self):
#     """
#     Updates the camera view in the y-axis.
#     """
#     maxCamera_y = int(HEIGHT * 2 / 3)
#     minCamera_y = int(HEIGHT / 3)
#
#     if self.playerOne.rect.top <= minCamera_y:
#         diff = minCamera_y - self.playerOne.rect.top
#         self.playerOne.rect.top = minCamera_y
#         self.scenario.shiftWorldY(diff)
#
#     if self.playerOne.rect.bottom >= maxCamera_y:
#         diff = maxCamera_y - self.playerOne.rect.bottom
#         self.playerOne.rect.bottom = maxCamera_y
#         self.scenario.shiftWorldY(diff)
#
#
#
#     def showLives(self, file_name, range_number):
#         self.life_icon = load_image(file_name, img_folder, alpha=True)
#         self.space = 25
#         for x in range(range_number):
#             self.screen.blit(self.life_icon, (self.space, 40))
#             self.space += 25
#
#
#
#             if event.key == pygame.K_ESCAPE:
#                 self.pause = not self.pause
#
#
#
#
#             # Ends game if playerOne loses
#             if self.playerOne.lives == 0:
#                 print("game over")
#                 self.showGameOverScreen()
#                 #raise Exception("GAME OVER")
#
#
#
#
#             # Restarts level upon being hit
#             if self.playerOne.isHit:
#                 self.playerOne.lives -= 1
#                 self.playerOne.isHit = False
#                 if self.level == 2:
#                     self.loadScenario02()
#                 if self.level == 3:
#                     self.loadScenario03()
#
#
#
#
#
#             # Changes level if complete
#             if self.scenario.isEnd:
#                 self.level += 1
#                 if self.level == 2:
#                     self.loadScenario02()
#                 if self.level == 3:
#                     self.loadScenario03()
#
#
#
#         spawn = (70, 70)
#         spawn = (70, 510)
#         spawn = (315, 180)

