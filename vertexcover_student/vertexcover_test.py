#! /usr/bin/env python3
from statistics import mean
import sys
import time

from search import random_walk
from vertexcover import State, VertexCover, maxvalue, randomized_maxvalue, read_instance


def elapsed_time(function, *args, **kwargs):
    start_time = time.monotonic()
    result = function(*args, **kwargs)
    end_time = time.monotonic()
    return end_time - start_time, result


def run_tests(filename):
    info = read_instance(filename)
    init_state = State(info[0], info[1], info[2])
    vc_problem = VertexCover(init_state)
    step_limit = 100

    mx_elaps_times = []
    mx_elaps_steps = []
    mx_elaps_values = []
    rnd_mx_elaps_times = []
    rnd_mx_elaps_steps = []
    rnd_mx_elaps_values = []
    rnd_w_elaps_times = []
    rnd_w_elaps_steps = []
    rnd_w_elaps_values = []

    for _ in range(10):
        mx_elaps, mx_result = elapsed_time(maxvalue, vc_problem, step_limit)
        mx_elaps_times.append(mx_elaps)
        mx_elaps_steps.append(mx_result[2])
        mx_elaps_values.append(mx_result[1])
        rnd_mx_elaps, rnd_max_result = elapsed_time(
            randomized_maxvalue, vc_problem, step_limit)
        rnd_mx_elaps_times.append(rnd_mx_elaps)
        rnd_mx_elaps_steps.append(rnd_max_result[2])
        rnd_mx_elaps_values.append(rnd_max_result[1])
        rnd_w_elaps, rnd_w_result = elapsed_time(
            random_walk, vc_problem, step_limit)
        rnd_w_elaps_times.append(rnd_w_elaps)
        rnd_w_elaps_steps.append(rnd_w_result[2])
        rnd_w_elaps_values.append(rnd_w_result[1])

    print(f'{filename[10:13]}', end=',')
    print(f'{mean(mx_elaps_times):.5f}', end=',')
    print(f'{mean(mx_elaps_steps)}', end=',')
    print(f'{mean(mx_elaps_values)}', end=',')
    print(f'{mean(rnd_mx_elaps_times):.5f}', end=',')
    print(f'{mean(rnd_mx_elaps_steps)}', end=',')
    print(f'{mean(rnd_mx_elaps_values)}', end=',')
    print(f'{mean(rnd_w_elaps_times):.5f}', end=',')
    print(f'{mean(rnd_w_elaps_steps)}', end=',')
    print(f'{mean(rnd_w_elaps_values)}')

    pass


if __name__ == '__main__':
    run_tests(sys.argv[1])
