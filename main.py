import pygame
import sys
from game import Game
from color import Colors
from agent import Agent
from blocks import *

pygame.init()

title_font = pygame.font.Font(None, 30)
score_text = title_font.render("Score:", True, Colors.white)
lines_text = title_font.render("Lines Cleared:", True, Colors.white)
pieces_text = title_font.render("Blocks Placed:", True, Colors.white)

score_background_rect = pygame.Rect(300, 0, 200, 600)

screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Tetris")

game = Game()

agent = Agent()

record = 0

number_of_episodes = 10000


while agent.n_games < number_of_episodes:
    old_state = game.get_properties()
    next_states = game.get_next_states()
    next_state = agent.decide_next_state(next_states)

    game.current_block.color = Colors.white
    game.play_step(next_state[0], next_state[1])

    reward, done, score = game.reward, game.game_over, game.score
    agent.remember(old_state, reward, next_states[next_state], done)

    if done:
        print(
            "Episode: ",
            agent.n_games,
            " Score: ",
            score,
            "Record: ",
            record,
            " Epsilon: ",
            agent.epsilon,
            " Lines cleared: ",
            game.cumulative_lines_cleared,
        )
        game.reset()
        agent.n_games = agent.n_games + 1
        agent.train()
        agent.reduce_epsilon()
        if score > record:
            record = score
            agent.model.save()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(Colors.black)
    pygame.draw.rect(screen, Colors.gray, score_background_rect)

    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    lines_value_surface = title_font.render(
        str(game.cumulative_lines_cleared), True, Colors.white
    )
    blocks_placed_value_surface = title_font.render(
        str(game.blocks_placed), True, Colors.white
    )
    screen.blit(score_text, (325, 50))
    screen.blit(score_value_surface, (325, 100))

    screen.blit(lines_text, (325, 150))
    screen.blit(lines_value_surface, (325, 200))

    screen.blit(pieces_text, (325, 250))
    screen.blit(blocks_placed_value_surface, (325, 300))

    game.render(screen)

    pygame.display.update()
