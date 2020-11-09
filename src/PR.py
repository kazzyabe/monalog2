import sick_ans

ans = sick_ans.ANSWERS_new

def load(file):
    f = open(file, 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    ans = {}
    for d in data:
        d = d.split('\t')
        if len(d) == 2:
            ans[int(d[0])] = d[1]
    
    return ans

fwd = "pred_monalog_preprocess_fwd.txt"
bwd = "pred_monalog_preprocess_bkwd.txt"

ans_fwd = load(fwd)
ans_bwd = load(bwd)

import pandas as pd
import numpy as np
'''0: U, 1: E, 2: C'''
p_U = [0,0,0]
p_E = [0,0,0]
p_C = [0,0,0]

def errs(true, pred):
    es = []
    for i in pred.keys():
        if pred[i] in ['U', 'E', 'C']:
            if pred[i] != true[i]:
                es.append(i)
    return es

def confMatrix(true, pred):
    '''0: U, 1: E, 2: C'''
    mat = {'U': [0,0,0], 'E': [0,0,0], 'C': [0,0,0]}
    k = {'U': 0, 'E': 1, 'C':2}
    for i in pred.keys():
        # print(i)
        # print(pred[i], true[i])
        if pred[i] in ['U', 'E', 'C']:
            mat[pred[i]][k[true[i]]] += 1
        i +=1
    return pd.DataFrame(np.array([mat['U'], mat['E'], mat['C']]),
                index=['U','E','C'],
                columns=['U', 'E', 'C'])

conf_fwd = confMatrix(ans, ans_fwd)
print(conf_fwd)
conf_bwd = confMatrix(ans, ans_bwd)
print(conf_bwd)

es = errs(ans, ans_fwd)

def preRec(conf):
    pre = []
    rec = [[0.,0.,0.] for i in range(3)]
    # get precision
    for i in range(len(conf)):
        t = 0.0
        tmp = []
        for j in range(len(conf.iloc[i])):
            tmp.append(conf.iloc[i,j])
            t += conf.iloc[i,j]
        for k in range(len(tmp)):
            tmp[k] = tmp[k]/t
        pre.append(tmp)

    # get recall
    for j in range(len(conf.iloc[0])):
        t = 0.0
        for i in range(len(conf)):
            rec[i][j] = conf.iloc[i,j]
            t += conf.iloc[i, j]
        for i in range(len(conf)):
            rec[i][j] = rec[i][j]/t
    pre = pd.DataFrame(np.array(pre),
                index=['U','E','C'],
                columns=['U', 'E', 'C'])
    rec = pd.DataFrame(np.array(rec),
                index=['U','E','C'],
                columns=['U', 'E', 'C'])
    return pre, rec

pre, rec = preRec(conf_fwd)

'''
>>> fwd
      U     E     C
U  5510  1474   480
E    32  1125     0
C    60     0  1125
>>> bwd
      U     E     C
U  5484  2043   480
E    62   559     1
C    60     0  1123
>>> pre
          U         E         C
U  0.738210  0.197481  0.064309
E  0.027658  0.972342  0.000000
C  0.050633  0.000000  0.949367
>>> rec
          U         E         C
U  0.983577  0.567141  0.299065
E  0.005712  0.432859  0.000000
C  0.010710  0.000000  0.700935

>>> es
[3, 4, 13, 20, 32, 33, 34, 38, 41, 43, 44, 55, 63, 64, 66, 67, 69, 87, 89, 100, 101, 107, 111, 118, 122, 141, 142, 143, 149, 153, 154, 156, 157, 158, 159, 160, 161, 164, 170, 172, 175, 177, 178, 181, 191, 193, 194, 196, 198, 200, 202, 204, 207, 208, 209, 210, 211, 218, 222, 230, 232, 233, 244, 247, 253, 254, 256, 265, 266, 276, 284, 293, 294, 300, 303, 304, 305, 311, 312, 313, 314, 322, 331, 340, 343, 351, 352, 354, 355, 357, 364, 373, 390, 391, 392, 395, 404, 406, 408, 410, 411, 414, 422, 424, 425, 431, 432, 433, 442, 445, 453, 456, 476, 477, 478, 480, 481, 482, 489, 491, 492, 494, 505, 506, 528, 529, 531, 532, 541, 544, 554, 555, 557, 567, 571, 580, 583, 585, 587, 590, 592, 593, 603, 612, 613, 614, 616, 626, 629, 642, 645, 648, 652, 665, 674, 675, 676, 677, 679, 680, 692, 693, 702, 703, 704, 705, 706, 713, 716, 717, 729, 740, 741, 750, 751, 752, 753, 774, 794, 796, 797, 798, 805, 806, 808, 809, 816, 818, 819, 828, 829, 830, 840, 853, 854, 858, 860, 865, 868, 870, 874, 876, 878, 880, 890, 891, 892, 894, 897, 898, 900, 902, 912, 914, 923, 924, 926, 927, 934, 937, 947, 951, 953, 956, 959, 960, 963, 964, 973, 974, 976, 977, 986, 987, 989, 990, 999, 1001, 1008, 1011, 1024, 1025, 1032, 1038, 1041, 1044, 1045, 1046, 1058, 1071, 1073, 1082, 1107, 1109, 1131, 1158, 1165, 1177, 1186, 1190, 1192, 1193, 1195, 1208, 1217, 1220, 1233, 1235, 1236, 1242, 1244, 1264, 1266, 1267, 1279, 1280, 1289, 1296, 1299, 1311, 1318, 1321, 1322, 1324, 1325, 1333, 1334, 1335, 1337, 1339, 1340, 1342, 1343, 1352, 1353, 1356, 1357, 1358, 1361, 1363, 1364, 1366, 1376, 1381, 1388, 1399, 1400, 1401, 1402, 1405, 1414, 1416, 1417, 1418, 1420, 1459, 1466, 1467, 1468, 1469, 1475, 1482, 1495, 1502, 1504, 1511, 1513, 1514, 1520, 1522, 1549, 1560, 1564, 1580, 1582, 1584, 1585, 1586, 1587, 1589, 1590, 1593, 1602, 1604, 1606, 1607, 1612, 1614, 1615, 1617, 1619, 1623, 1627, 1631, 1641, 1644, 1646, 1652, 1654, 1657, 1658, 1659, 1660, 1663, 1664, 1669, 1677, 1678, 1683, 1684, 1686, 1687, 1689, 1690, 1693, 1696, 1700, 1702, 1705, 1722, 1726, 1734, 1735, 1737, 1746, 1750, 1751, 1753, 1754, 1755, 1757, 1758, 1760, 1761, 1765, 1766, 1769, 1777, 1780, 1782, 1784, 1786, 1788, 1792, 1793, 1796, 1798, 1801, 1802, 1803, 1820, 1829, 1830, 1842, 1843, 1851, 1852, 1857, 1860, 1865, 1866, 1868, 1869, 1871, 1872, 1876, 1878, 1881, 1884, 1888, 1889, 1898, 1901, 1909, 1922, 1923, 1956, 1964, 1968, 1970, 1972, 1973, 1980, 1991, 2004, 2014, 2027, 2036, 2058, 2059, 2060, 2063, 2064, 2067, 2078, 2084, 2087, 2101, 2117, 2121, 2139, 2152, 2153, 2154, 2164, 2166, 2167, 2168, 2170, 2174, 2176, 2178, 2179, 2181, 2184, 2186, 2187, 2188, 2191, 2202, 2214, 2218, 2219, 2220, 2222, 2225, 2235, 2243, 2250, 2251, 2252, 2254, 2255, 2258, 2272, 2273, 2281, 2282, 2284, 2286, 2288, 2300, 2305, 2309, 2312, 2318, 2325, 2328, 2337, 2340, 2343, 2344, 2345, 2346, 2349, 2350, 2363, 2364, 2367, 2368, 2370, 2374, 2377, 2401, 2405, 2406, 2415, 2416, 2417, 2420, 2423, 2425, 2428, 2430, 2437, 2440, 2441, 2442, 2445, 2446, 2447, 2449, 2455, 2458, 2465, 2486, 2489, 2498, 2509, 2517, 2518, 2519, 2526, 2532, 2534, 2536, 2545, 2546, 2550, 2557, 2561, 2563, 2566, 2573, 2579, 2587, 2588, 2590, 2591, 2593, 2595, 2622, 2627, 2628, 2629, 2631, 2632, 2633, 2635, 2638, 2641, 2643, 2648, 2652, 2653, 2664, 2686, 2689, 2693, 2697, 2699, 2701, 2711, 2722, 2733, 2742, 2746, 2748, 2750, 2751, 2753, 2756, 2759, 2762, 2763, 2769, 2772, 2774, 2776, 2779, 2791, 2793, 2794, 2795, 2797, 2809, 2811, 2813, 2815, 2827, 2831, 2833, 2835, 2836, 2840, 2843, 2844, 2850, 2851, 2853, 2854, 2856, 2858, 2864, 2865, 2867, 2868, 2874, 2876, 2897, 2901, 2903, 2905, 2907, 2912, 2913, 2917, 2935, 2937, 2938, 2940, 2946, 2947, 2950, 2952, 2953, 2954, 2964, 2968, 2969, 2971, 2974, 2978, 2979, 2988, 2994, 2997, 2999, 3001, 3003, 3011, 3015, 3024, 3025, 3026, 3027, 3029, 3035, 3037, 3045, 3047, 3054, 3055, 3062, 3065, 3066, 3067, 3069, 3070, 3075, 3077, 3078, 3079, 3082, 3089, 3091, 3092, 3103, 3106, 3108, 3109, 3112, 3113, 3114, 3115, 3116, 3117, 3119, 3120, 3122, 3123, 3126, 3139, 3149, 3167, 3171, 3175, 3180, 3182, 3184, 3194, 3198, 3199, 3200, 3201, 3202, 3207, 3208, 3209, 3211, 3212, 3214, 3216, 3218, 3223, 3230, 3233, 3246, 3250, 3268, 3272, 3273, 3275, 3280, 3283, 3285, 3297, 3301, 3304, 3307, 3308, 3310, 3314, 3315, 3317, 3320, 3323, 3337, 3344, 3368, 3370, 3372, 3373, 3386, 3388, 3389, 3390, 3391, 3392, 3395, 3400, 3403, 3407, 3409, 3415, 3435, 3437, 3439, 3440, 3441, 3442, 3444, 3449, 3451, 3453, 3463, 3473, 3480, 3483, 3504, 3508, 3509, 3510, 3512, 3515, 3524, 3527, 3536, 3556, 3562, 3563, 3564, 3567, 3568, 3569, 3570, 3571, 3572, 3574, 3580, 3586, 3588, 3595, 3598, 3600, 3615, 3619, 3620, 3621, 3623, 3626, 3627, 3629, 3632, 3639, 3641, 3643, 3644, 3659, 3670, 3677, 3679, 3681, 3688, 3693, 3695, 3696, 3698, 3700, 3702, 3703, 3704, 3705, 3707, 3714, 3725, 3726, 3731, 3733, 3742, 3745, 3747, 3754, 3756, 3757, 3758, 3761, 3763, 3768, 3772, 3774, 3776, 3792, 3798, 3800, 3801, 3815, 3817, 3818, 3836, 3849, 3850, 3853, 3856, 3870, 3875, 3880, 3881, 3884, 3896, 3906, 3907, 3909, 3911, 3912, 3913, 3919, 3920, 3924, 3938, 3940, 3941, 3942, 3943, 3945, 3946, 3947, 3949, 3950, 3951, 3954, 3957, 3960, 3962, 3974, 3976, 4006, 4008, 4011, 4016, 4017, 4022, 4026, 4027, 4043, 4064, 4066, 4076, 4079, 4090, 4092, 4094, 4097, 4108, 4111, 4113, 4115, 4116, 4118, 4120, 4125, 4134, 4136, 4139, 4147, 4163, 4181, 4183, 4187, 4192, 4201, 4203, 4205, 4206, 4207, 4209, 4212, 4221, 4222, 4230, 4246, 4249, 4252, 4254, 4255, 4256, 4259, 4270, 4272, 4274, 4275, 4277, 4279, 4280, 4281, 4282, 4283, 4284, 4288, 4291, 4292, 4320, 4329, 4333, 4344, 4391, 4393, 4394, 4395, 4396, 4397, 4407, 4408, 4409, 4410, 4418, 4419, 4425, 4458, 4459, 4460, 4463, 4490, 4494, 4505, 4507, 4542, 4548, 4550, 4553, 4555, 4564, 4566, 4568, 4569, 4570, 4571, 4572, 4573, 4589, 4591, 4600, 4602, 4604, 4606, 4643, 4649, 4652, 4654, 4671, 4673, 4675, 4680, 4690, 4692, 4699, 4701, 4706, 4708, 4710, 4711, 4720, 4728, 4732, 4733, 4734, 4735, 4736, 4737, 4739, 4742, 4745, 4747, 4780, 4784, 4786, 4800, 4812, 4826, 4828, 4829, 4830, 4831, 4832, 4842, 4884, 4886, 4889, 4892, 4893, 4895, 4907, 4921, 4935, 4941, 4944, 4954, 4956, 4957, 4972, 4973, 4974, 4999, 5003, 5005, 5006, 5007, 5012, 5016, 5022, 5024, 5027, 5028, 5030, 5033, 5036, 5043, 5045, 5047, 5059, 5062, 5063, 5095, 5106, 5107, 5108, 5110, 5111, 5113, 5134, 5135, 5136, 5137, 5138, 5140, 5147, 5149, 5158, 5159, 5165, 5178, 5179, 5180, 5181, 5182, 5186, 5194, 5195, 5198, 5212, 5226, 5228, 5260, 5264, 5268, 5271, 5272, 5273, 5277, 5280, 5281, 5282, 5284, 5286, 5287, 5288, 5289, 5290, 5291, 5314, 5326, 5327, 5337, 5394, 5396, 5397, 5398, 5401, 5428, 5430, 5431, 5432, 5434, 5435, 5457, 5459, 5462, 5466, 5467, 5469, 5470, 5516, 5534, 5552, 5554, 5555, 5567, 5568, 5569, 5570, 5572, 5573, 5574, 5576, 5577, 5578, 5590, 5592, 5593, 5594, 5597, 5606, 5621, 5622, 5623, 5626, 5637, 5639, 5641, 5646, 5701, 5702, 5703, 5704, 5709, 5710, 5723, 5727, 5729, 5731, 5732, 5743, 5750, 5759, 5760, 5761, 5781, 5792, 5793, 5798, 5809, 5817, 5855, 5862, 5863, 5864, 5866, 5868, 5871, 5875, 5877, 5880, 5898, 5934, 5937, 5941, 5961, 5964, 5972, 5975, 5983, 5997, 6006, 6007, 6009, 6011, 6014, 6017, 6025, 6027, 6040, 6045, 6047, 6056, 6076, 6079, 6080, 6082, 6085, 6092, 6094, 6096, 6100, 6101, 6114, 6118, 6125, 6126, 6132, 6135, 6136, 6143, 6145, 6146, 6161, 6162, 6174, 6179, 6183, 6184, 6186, 6192, 6193, 6194, 6195, 6201, 6202, 6204, 6212, 6214, 6217, 6218, 6220, 6221, 6223, 6230, 6232, 6250, 6251, 6253, 6257, 6259, 6260, 6265, 6266, 6267, 6269, 6277, 6278, 6279, 6282, 6284, 6286, 6287, 6288, 6290, 6297, 6299, 6316, 6317, 6324, 6325, 6326, 6332, 6335, 6336, 6338, 6343, 6345, 6356, 6357, 6359, 6365, 6366, 6370, 6388, 6395, 6404, 6417, 6428, 6429, 6437, 6438, 6454, 6457, 6468, 6470, 6474, 6476, 6477, 6479, 6485, 6489, 6495, 6498, 6506, 6509, 6518, 6528, 6535, 6537, 6541, 6542, 6543, 6544, 6555, 6556, 6557, 6564, 6573, 6575, 6584, 6586, 6587, 6593, 6602, 6604, 6613, 6614, 6620, 6629, 6632, 6634, 6637, 6639, 6640, 6643, 6649, 6660, 6661, 6663, 6670, 6671, 6678, 6680, 6681, 6683, 6689, 6690, 6693, 6695, 6696, 6698, 6705, 6720, 6734, 6736, 6745, 6746, 6747, 6753, 6763, 6783, 6785, 6794, 6804, 6812, 6814, 6819, 6820, 6821, 6841, 6843, 6854, 6856, 6860, 6863, 6870, 6872, 6873, 6874, 6878, 6881, 6888, 6890, 6899, 6902, 6908, 6909, 6917, 6918, 6930, 6932, 6935, 6946, 6948, 6949, 6968, 6977, 6979, 6984, 6988, 6990, 6991, 6997, 6998, 6999, 7008, 7010, 7011, 7012, 7014, 7015, 7018, 7032, 7039, 7046, 7057, 7059, 7060, 7066, 7073, 7085, 7093, 7094, 7096, 7099, 7100, 7101, 7102, 7105, 7111, 7115, 7121, 7126, 7127, 7128, 7130, 7131, 7134, 7136, 7137, 7138, 7141, 7142, 7153, 7158, 7161, 7162, 7173, 7175, 7182, 7184, 7187, 7188, 7190, 7191, 7192, 7202, 7212, 7224, 7225, 7237, 7242, 7244, 7255, 7259, 7260, 7261, 7263, 7265, 7266, 7272, 7274, 7275, 7279, 7284, 7295, 7297, 7300, 7301, 7303, 7304, 7308, 7309, 7310, 7311, 7312, 7314, 7317, 7320, 7324, 7327, 7334, 7335, 7337, 7346, 7347, 7354, 7355, 7360, 7366, 7368, 7369, 7379, 7382, 7385, 7397, 7406, 7413, 7416, 7418, 7420, 7421, 7423, 7424, 7426, 7442, 7445, 7447, 7459, 7466, 7471, 7473, 7474, 7476, 7477, 7478, 7479, 7484, 7497, 7508, 7509, 7510, 7515, 7517, 7525, 7527, 7535, 7546, 7550, 7551, 7552, 7554, 7569, 7570, 7572, 7574, 7575, 7580, 7582, 7585, 7586, 7595, 7596, 7597, 7600, 7603, 7605, 7607, 7608, 7615, 7632, 7635, 7637, 7640, 7641, 7646, 7647, 7650, 7658, 7666, 7668, 7670, 7672, 7674, 7675, 7677, 7686, 7689, 7692, 7694, 7698, 7699, 7708, 7722, 7737, 7747, 7748, 7755, 7757, 7759, 7766, 7775, 7786, 7788, 7815, 7842, 7845, 7849, 7878, 7879, 7880, 7882, 7883, 7884, 7885, 7886, 7889, 7893, 7896, 7902, 7922, 7923, 7924, 7925, 7926, 7927, 7936, 7937, 7952, 7954, 7955, 7956, 7957, 7960, 7961, 7964, 7965, 7981, 7984, 7987, 7989, 7991, 8001, 8010, 8011, 8012, 8019, 8021, 8023, 8027, 8039, 8046, 8048, 8054, 8055, 8057, 8064, 8068, 8069, 8072, 8073, 8075, 8082, 8088, 8090, 8091, 8100, 8101, 8103, 8109, 8120, 8127, 8136, 8156, 8158, 8160, 8165, 8166, 8172, 8174, 8182, 8183, 8189, 8190, 8193, 8206, 8210, 8211, 8217, 8219, 8230, 8235, 8244, 8253, 8256, 8257, 8263, 8266, 8268, 8270, 8271, 8273, 8274, 8275, 8280, 8282, 8286, 8289, 8300, 8302, 8303, 8316, 8318, 8326, 8327, 8332, 8338, 8340, 8342, 8345, 8349, 8363, 8364, 8371, 8372, 8380, 8381, 8388, 8391, 8399, 8410, 8412, 8413, 8414, 8415, 8417, 8424, 8443, 8444, 8446, 8455, 8458, 8469, 8480, 8484, 8485, 8501, 8503, 8508, 8514, 8515, 8519, 8520, 8521, 8522, 8523, 8542, 8543, 8544, 8547, 8549, 8551, 8552, 8562, 8568, 8570, 8571, 8576, 8579, 8581, 8583, 8585, 8588, 8597, 8604, 8606, 8608, 8609, 8610, 8611, 8612, 8613, 8615, 8622, 8624, 8625, 8633, 8634, 8640, 8643, 8651, 8652, 8659, 8662, 8678, 8680, 8688, 8689, 8690, 8691, 8693, 8695, 8696, 8707, 8714, 8716, 8717, 8736, 8739, 8740, 8741, 8743, 8750, 8752, 8760, 8770, 8778, 8779, 8786, 8790, 8794, 8795, 8798, 8800, 8803, 8813, 8817, 8819, 8821, 8840, 8842, 8850, 8856, 8858, 8860, 8871, 8905, 8907, 8909, 8911, 8912, 8917, 8919, 8920, 8923, 8930, 8933, 8935, 8939, 8948, 8959, 8960, 8967, 8975, 8984, 8996, 9014, 9015, 9031, 9040, 9044, 9046, 9048, 9049, 9051, 9058, 9060, 9069, 9070, 9078, 9087, 9094, 9095, 9096, 9103, 9105, 9112, 9114, 9115, 9123, 9130, 9132, 9136, 9141, 9143, 9144, 9145, 9146, 9147, 9148, 9150, 9157, 9177, 9179, 9181, 9182, 9183, 9193, 9202, 9204, 9213, 9221, 9233, 9235, 9237, 9240, 9247, 9256, 9258, 9265, 9267, 9275, 9276, 9277, 9285, 9292, 9312, 9319, 9320, 9321, 9322, 9330, 9334, 9338, 9341, 9342, 9348, 9349, 9360, 9377, 9378, 9386, 9395, 9402, 9404, 9411, 9413, 9420, 9422, 9425, 9426, 9432, 9433, 9434, 9435, 9437, 9450, 9460, 9471, 9473, 9478, 9480, 9486, 9487, 9489, 9490, 9491, 9493, 9494, 9495, 9510, 9511, 9521, 9530, 9532, 9533, 9539, 9541, 9550, 9552, 9553, 9554, 9555, 9556, 9561, 9562, 9563, 9564, 9565, 9571, 9572, 9575, 9577, 9584, 9597, 9601, 9613, 9615, 9616, 9624, 9636, 9641, 9653, 9660, 9662, 9664, 9665, 9666, 9668, 9671, 9678, 9689, 9696, 9706, 9708, 9711, 9713, 9716, 9720, 9732, 9741, 9744, 9747, 9749]
'''