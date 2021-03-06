import logging

from judge_one import judge_one
from judge_result import judge_result
# from main import low_level


def judge(id, question_id, data_count, time_limit, mem_limit, program_info, result_code, language, dblock):
    # low_level()
    """评测编译类型语言"""
    max_mem = 0
    max_time = 0
    # if language in ["java", 'python2', 'python3', 'ruby', 'perl']:
    #     time_limit = time_limit * 2
    #     mem_limit = mem_limit * 2
    for i in range(data_count):
        # print('data count(%s): %s' % (data_count, i))
        ret = judge_one(
            id,
            question_id,
            i + 1,
            time_limit + 10,
            mem_limit,
            language,
            dblock
        )
        # print(ret)
        if ret is False:
            continue
        if ret['result'] == 5:
            program_info['result'] = result_code["Runtime Error"]
            return program_info
        elif ret['result'] == 2:
            program_info['result'] = result_code["Time Limit Exceeded"]
            program_info['take_time'] = time_limit + 10
            return program_info
        elif ret['result'] == 3:
            program_info['result'] = result_code["Memory Limit Exceeded"]
            program_info['take_memory'] = mem_limit
            # print(program_info)
            return program_info
        if max_time < ret["timeused"]:
            max_time = ret['timeused']
        if max_mem < ret['memoryused']:
            max_mem = ret['memoryused']
        result = judge_result(id, question_id, i + 1)
        if result is False:
            continue
        if result == "Wrong Answer" or result == "Output limit":
            program_info['result'] = result_code[result]
            break
        elif result == 'Presentation Error':
            program_info['result'] = result_code[result]
        elif result == 'Accepted':
            if program_info['result'] != 'Presentation Error':
                program_info['result'] = result_code[result]
        else:
            logging.error("judge did not get result")
    program_info['take_time'] = max_time
    program_info['take_memory'] = max_mem
    # print('return program_info')
    return program_info

