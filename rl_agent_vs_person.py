from tensorflow.keras.models import load_model
from keras_rl_agent import SimpleRLPlayer
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory

from threading import Thread
import asyncio


if __name__ == '__main__':
    model = load_model("model_10000.h5")
    memory = SequentialMemory(limit=10000, window_length=1)
    env_player = SimpleRLPlayer(battle_format="gen8randombattle")
    # Simple epsilon greedy
    policy = LinearAnnealedPolicy(
        EpsGreedyQPolicy(),
        attr="eps",
        value_max=1.0,
        value_min=0.05,
        value_test=0,
        nb_steps=10000,
    )

    # Defining our DQN
    dqn = DQNAgent(
        model=model,
        nb_actions=len(env_player.action_space),
        policy=policy,
        memory=memory,
        nb_steps_warmup=1000,
        gamma=0.5,
        target_model_update=1,
        delta_clip=0.01,
        enable_double_dqn=True,
    )

    dqn.compile(Adam(lr=0.00025), metrics=["mae"])

    def play():
        env_player.reset_battles()
        dqn.test(env_player, nb_episodes=1, visualize=False, verbose=False)
        env_player._start_new_battle = False

    thread = Thread(target=play)
    thread.start()

    loop = asyncio.get_event_loop()
    print(f"Challenge to {env_player.username}")

    async def accept():
        await env_player.accept_challenges(None, 1)

    loop.run_until_complete(accept())
    thread.join()
