import numpy as np
import time
import os
from sqlalchemy import null
import pandas as pd


class FISTA_PROJ_BACK:

    # 初期設定
    def __init__(self):
        # 結果格納用
        self.iter = null
        self.sol = null
        self.sol_obj = null
        self.num_call_nbl = null
        self.num_call_obj = null
        self.num_call_conv = null
        self.num_call_proj = null
        self.lips = null
        self.total_time = null
        # 演算等に必要なデータ
        self.obj_func = null
        self.nbl_func = null
        self.proj_func = null
        self.conv_func = null
        self.lips_init = null
        self.x_init = null
        self.conv_judge = null
        self.back_para = null
        self.output_iter = 1000
        # 結果格納用のデータセット
        self.output_data = null
        self.output_root = "."

    # 目的関数と勾配関数を設定(関数の引数はベクトルのみ)
    def set_obj_func(self, obj_func):
        self.obj_func = obj_func

    def set_nbl_func(self, nbl_func):
        self.nbl_func = nbl_func

    def set_proj_func(self, proj_func):
        self.proj_func = proj_func

    def set_conv_func(self, conv_func):
        self.conv_func = conv_func

    # 計算に必要な各種設定をsetting
    def set_lips_init(self, lips_init):
        self.lips_init = lips_init

    def set_output_iter(self, iter):
        self.output_iter = iter

    def set_conv_judge(self, conv):
        self.conv_judge = conv

    def set_back_para(self, para):
        if para <= 1.0:
            print("backtracking parameter is rather than 1.")
            return 0
        self.back_para = para

    def set_x_init(self, x_init):
        self.x_init = x_init

    def set_output_root(self, root):
        self.output_root = root
        os.makedirs(root, exist_ok=True)

    # FISTA with backtracking
    def exect_FISTA_proj_back(self):

        is_Executed = 0

        print("\n\n")

        if self.x_init is null:
            print("init sol is not set.")
            is_Executed = -1
        if self.obj_func is null:
            print("objective function is not set.")
            is_Executed = -1
        if self.nbl_func is null:
            print("nabla function is not set.")
            is_Executed = -1
        if self.proj_func is null:
            print("projection function is not set.")
            is_Executed = -1
        if self.conv_func is null:
            print("convergence function is not set.")
            is_Executed = -1
        if self.lips_init is null:
            print("initial lipschitz constant (>0) is not set.")
            is_Executed = -1
        if self.back_para is null:
            print("backtracking parameter is not set.")
            is_Executed = -1
        if self.conv_judge is null:
            print("convergence judgement (>0) is not set.")
            is_Executed = -1

        if is_Executed:
            print("FISTA with backtracking cannot be executed.\n\n")
            return -1

        print('start Accel Gradient Projection Method (FISTA with backtracking)!')

        # 初期状態の諸々を計算
        [now_obj, temp_total_time] = self.obj_func(self.x_init)
        [now_conv, temp_total_time] = self.conv_func(self.x_init)

        output_data = pd.DataFrame([[0, 0.0, now_obj, now_conv, self.lips_init, 0, 0, 0, 0]], columns=['Iteration', 'total_time', 'now_obj', 'now_conv', 'now_lips', 'num_call_obj', 'num_call_nbl', 'num_call_proj', 'num_call_conv'])
        if self.output_root != null:
            output_data.to_csv(os.path.join(self.output_root, 'result.csv'))


        # 初期設定（反復回数・勾配関数の呼び出し回数を初期化）
        iteration = 0
        num_call_obj = 0
        num_call_nbl = 0
        num_call_conv = 0
        num_call_proj = 0
        now_lips = self.lips_init

        # 解の更新で使用する値
        t = 1.0
        j = 0

        # 初期解の設定
        now_sol = self.x_init.copy()

        temp_sol = now_sol.copy()

        # 計算時間格納用変数
        total_time = 0.0

        if len(now_sol) > 5:
            print('iteration:', iteration, ' now_sol:', now_sol[:5], ' now_obj:', now_obj, ' convergence:', now_conv)
        else:
            print('iteration:', iteration, ' now_sol:', now_sol, ' now_obj:', now_obj, ' convergence:', now_conv)


        while 1:

            iteration += 1

            # 勾配計算（一時的な解の）
            [temp_nbl, temp_total_time] = self.nbl_func(temp_sol)
            total_time += temp_total_time
            num_call_nbl += 1

            # backtracking
            [now_lips, temp_call_obj, temp_call_nbl, temp_call_proj, temp_total_time] = self.backtracking(temp_sol, now_lips)
            total_time += temp_total_time
            num_call_obj += temp_call_obj
            num_call_nbl += temp_call_nbl
            num_call_proj += temp_call_proj

            # 暫定解の更新
            prev_sol = now_sol
            [now_sol, temp_total_time] = self.proj_func(temp_sol - temp_nbl/now_lips)
            total_time += temp_total_time
            num_call_proj += 1

            prev_obj = now_obj
            [now_obj, temp_total_time] = self.obj_func(now_sol)
            total_time += temp_total_time
            num_call_obj += 1

            start_time = time.process_time()
            prev_t = t
            t = (1.0 + (1.0 + 4.0*prev_t**2.0)**(1.0/2.0))/2.0
            j += 1
            temp_sol = now_sol + ((prev_t - 1.0)/t) * (now_sol - prev_sol)
            if now_obj - prev_obj > 0 and j > 5:
                t = 1.0
                j = 0
            end_time = time.process_time()
            total_time += end_time - start_time

            
            # 収束判定の準備
            [conv, temp_total_time] = self.conv_func(now_sol)
            total_time += temp_total_time
            num_call_conv += 1

            if iteration % self.output_iter == 0:

                if len(now_sol) > 5:
                    print('iteration:', iteration, ' now_sol:', now_sol[:5], ' now_obj:', now_obj, ' convergence:', conv)
                else:
                    print('iteration:', iteration, ' now_sol:', now_sol, ' now_obj:', now_obj, ' convergence:', conv)

                add_df = pd.DataFrame([[iteration, total_time, now_obj, conv, now_lips, num_call_obj, num_call_nbl, num_call_proj, num_call_conv]], columns=output_data.columns)
                output_data = output_data.append(add_df)
                if self.output_root != null:
                    output_data.to_csv(os.path.join(self.output_root, 'result.csv'))

            # 収束判定
            if conv < self.conv_judge:
                break

        self.sol = now_sol
        self.iter = iteration
        self.total_time = total_time
        self.num_call_nbl = num_call_nbl
        self.num_call_obj = num_call_obj
        self.num_call_proj = num_call_proj
        self.num_call_conv = num_call_conv
        [self.sol_obj, dummy_total_time] = self.obj_func(self.sol)

        if self.output_root != null:
            np.savetxt(os.path.join(self.output_root, 'sol.csv'), self.sol)
            if iteration % self.output_iter != 0:
                add_df = pd.DataFrame([[self.iter, self.total_time, self.sol_obj, conv, now_lips, self.num_call_obj, self.num_call_nbl, self.num_call_proj, self.num_call_conv]], columns=output_data.columns)
                output_data = output_data.append(add_df)
                self.output_data = output_data
                output_data.to_csv(os.path.join(self.output_root, 'result.csv'))

        print('finish accel gradient projection method')

        return 0



    def backtracking(self, now_sol, now_lips):

        total_time = 0.0
        
        [now_obj, temp_total_time] = self.obj_func(now_sol)
        total_time += temp_total_time
        [now_nbl, temp_total_time] = self.nbl_func(now_sol)
        total_time += temp_total_time
        num_call_obj = 1
        num_call_nbl = 1
        num_call_proj = 0

        start_time = time.process_time()

        iota = 0
        while 1:

            [temp_sol, temp_total_time] = self.proj_func(now_sol - now_nbl/(self.back_para**iota * now_lips))
            num_call_proj += 1
            end_time = time.process_time()
            total_time += end_time - start_time

            [F, temp_total_time] = self.obj_func(temp_sol)
            total_time += temp_total_time
            num_call_obj += 1

            start_time = time.process_time()
            now_nbl_nolm = np.dot(temp_sol-now_sol, temp_sol-now_sol)
            Q = now_obj + np.dot(now_nbl, temp_sol - now_sol) + now_nbl_nolm * (self.back_para**iota*now_lips/2.0)

            # print('F: ', F, 'Q: ', Q)

            if F <= Q:
                break

            iota += 1

        end_time = time.process_time()
        total_time += end_time - start_time

        return [self.back_para**iota*now_lips, num_call_obj, num_call_nbl, num_call_proj, total_time]


# 目的関数
def obj_func(x):
    start_time = time.process_time()
    obj = 0
    for i in range(len(x)):
        obj += (x[i] - 5.0)**2
    end_time = time.process_time()
    return obj, end_time-start_time

# 勾配関数
def nbl_func(x):
    start_time = time.process_time()
    nbl_vec = x*2.0 - 10.0
    end_time = time.process_time()
    return nbl_vec, end_time-start_time

# 射影関数
def proj_func(x):
    start_time = time.process_time()
    x = x.clip(0.0)
    end_time = time.process_time()
    return x, end_time-start_time

# 収束判定値関数
def conv_func(x):
    [now_nbl, total_time] = nbl_func(x)
    start_time = time.process_time()
    conv_vec = -x * now_nbl
    min_conv = np.min(conv_vec)
    max_conv = np.max(conv_vec)
    if max_conv > -min_conv:
        conv = max_conv
    else:
        conv = -min_conv
    end_time = time.process_time()
    return conv, end_time-start_time

# 初期解
x_init = np.array([-10, 2, 3, 7, 8, 9, 0])



# 最適化クラスの作成
fista_proj_back = FISTA_PROJ_BACK()

# 関数の設定
fista_proj_back.set_obj_func(obj_func)
fista_proj_back.set_nbl_func(nbl_func)
fista_proj_back.set_proj_func(proj_func)
fista_proj_back.set_conv_func(conv_func)

# 各種パラメータを設定
fista_proj_back.set_lips_init(0.0003)
fista_proj_back.set_output_iter(1) # 無くてもよい
fista_proj_back.set_conv_judge(0.00001)
fista_proj_back.set_back_para(1.1) # 1以上の定数
fista_proj_back.set_x_init(x_init)
fista_proj_back.set_output_root("./result")

# 最適化実行
fista_proj_back.exect_FISTA_proj_back()
