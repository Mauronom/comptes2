def calcular_stats(moviments, date_inici=None, date_fi=None):
    moviments.sort(key=lambda m: m.data)
    total = float(sum(m.import_ for m in moviments))
    d_ini = min(moviments[0].data,date_inici) if date_inici and moviments else moviments[0].data if moviments else None
    d_fi = max(moviments[-1].data,date_fi) if date_fi and moviments else moviments[-1].data if moviments else None
    dies_diferents = 0
    if d_ini and d_fi:
        dies_diferents = (d_fi - d_ini).days + 1 if moviments else 0
    diari = total / dies_diferents if dies_diferents > 0 else 0
    mensual = diari * 30
    return total, diari, mensual