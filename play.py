from env import Env, View
from dqn.config import HYPER_PARAMS
from dqn import make_env

import argparse


class Play(View):
    def __init__(self, name, env, args):
        super(Play, self).__init__(name, make_env(env=env, max_episode_steps=args.max_steps))

        self.player = args.player

        self.ep = 0

        print()
        print("PLAY")
        print()
        [print(arg, "=", getattr(args, arg)) for arg in vars(args)]

        self.max_episodes = args.max_episodes

    def setup(self):
        _ = self.env.reset()

    def loop(self):
        action = self.get_play_action()

        _, _, done, info = self.env.step(action)
        if done:
            self.setup()

            self.ep += 1

            Env.ep_info_log_csv(info, ep=self.ep, log_dir=self.player)

            if bool(self.max_episodes) and self.ep >= self.max_episodes:
                exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PLAY")
    parser.add_argument('-max_steps', type=int, default=HYPER_PARAMS['max_episode_steps'], help='Max episode steps')
    parser.add_argument('-max_episodes', type=int, default=HYPER_PARAMS['max_episodes'], help='Max episodes')
    parser.add_argument('-player', type=str, default='player', help='Player')

    Play("PLAY", Env("play"), parser.parse_args()).run()
