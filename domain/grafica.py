from collections import defaultdict
from datetime import datetime, time

def calcular_punts(moviments):
    comptadors = defaultdict(int)
    punts = []
    bancs = []
    for m in moviments:
        if m.banc not in bancs:
            bancs.append(m.banc)
        hora = comptadors[(m.data, m.banc)]
        dt = datetime.combine(m.data, time(hour=hora))
        punts.append((dt, m.balance, m.banc, m.concepte, m.import_))
        comptadors[(m.data, m.banc)] += 1
    sorted_punts = sorted(punts, key=lambda p: (p[0], p[2]))
    # Afegir punts totals per data
    per_data = defaultdict(float)
    aux = {}
    for b in bancs:
        aux[b] = 0
        aux['import_'] = 0
    per_data_i = [aux]
    dt_ant = None
    for dt, balance, banc, concepte, import_ in sorted_punts:
        if dt != dt_ant:
            aux = {}
            for b in bancs:
                aux[b] = 0
                aux['import_'] = 0
            aux['data'] = dt
            per_data_i.append(aux)
            dt_ant = dt
        per_data_i[len(per_data_i)-1][banc] += balance
        per_data_i[len(per_data_i)-1]['import_'] += import_
    # per_data_i[len(per_data_i)-1]['Total'] = sum(per_data_i[len(per_data_i)-1][b] for b in bancs)
    i = 1
    for e in per_data_i[1:]:
        for b in bancs:
            if e[b]==0:
                e[b] = per_data_i[i-1][b]
        e["Total"] = sum(e[b] for b in bancs)
        sorted_punts.append((e['data'], e["Total"], "Total", "Total", e['import_']))
        i = i+1
    
    sorted_punts = sorted(sorted_punts, key=lambda p: (p[0], p[2]))
    return sorted_punts
    