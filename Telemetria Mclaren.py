# Databricks notebook source
import pandas as pd
import numpy as np
import random

# 1. DADOS GEOMÉTRICOS E MATEMÁTICA (Exatamente o seu código)
dados_brutos = """
0,09550722281063373; 0,8384744861410812
0,0835094905138809; 0,8257164579881605
0,039276092870358714; 0,7512074640837118
-0,015091653006244932; 0,6534676962156605
-0,025349054903908153; 0,6403624809376691
-0,028583608372922953; 0,6208057378165887
-0,012520710371226595; 0,5847729879627149
0,007084375260939746; 0,5429830845158938
0,04403123805170894; 0,5027840891611697
0,08073199351331395; 0,4828362111776676
0,11923460620629966; 0,45747836672628917
0,1526392813665991; 0,4230365249645123
0,17575579121308937; 0,3780208575961468
0,1954224036775467; 0,3311681748065203
0,23973051247456545; 0,2566723652232765
0,3173202427673012; 0,15786027256386692
0,4209534022140873; 0,05890315237120025
0,5275442443845781; 0,0022852823422387925
0,7103404631212564; -0,03923214513300777
1,056573922291611; -0,10072821400790177
1,19054859960535; -0,12493023296695571
1,2113095107298406; -0,11897091978219487
1,2145133007827096; -0,09688278698971176
1,1895641702886932; -0,04392576348206689
1,101071006359238; 0,09494029699880913
1,0604896656895626; 0,14849061496068905
1,0023819673644105; 0,2156383628588885
0,9427185191370424; 0,267944959853742
0,41626417863876286; 0,5876164065693078
0,35653920357910374; 0,6449857829069672
0,3123849118628128; 0,7068246441331969
0,25201390506409793; 0,8173532035703143
0,25332354763715004; 0,8524454718448822
0,3132199188724769; 0,9238297816236932
0,33581345064449364; 0,9218477386691748
0,3655836479258867; 0,9007572195145535
0,395599952536444; 0,8594155829887099
0,4064110959247267; 0,8269557841814514
0,4456212671890589; 0,7433759772878095
0,48256812997982834; 0,7031769819330853
0,5211015060889592; 0,6752877478103041
0,5540447300070757; 0,6788167511195687
0,55547742624471; 0,7037834607085255
0,5085676113965274; 0,8495053682161176
0,5338419551469396; 0,9126450824679292
0,5406186962464239; 0,9264446719960624
0,5597930940525531; 0,9200942239488801
0,579029018690973; 0,9086809965588922
0,5984187604101205; 0,8846108208118906
0,6161296985624698; 0,8558250528471543
0,6181161362907235; 0,8352267483508613
0,6545839687443695; 0,6915879635936945
0,6865251842508893; 0,6347108019143636
0,7360235208290304; 0,5617048206273101
0,7905890315237121; 0,5003142263220579
0,8484198591035543; 0,4559489854664833
1,0773260438686318; 0,33452578194011684
1,1052943839186442; 0,3188452292533721
1,119124736862923; 0,3236619012670132
1,1100231604575845; 0,35830590262060347
1,0868758871949482; 0,40585295966037194
0,9982289061847653; 0,557375968498262
0,8468069771427822; 0,7315232725243141
0,6623802973503912; 0,9072043525839073
0,5993284785732809; 0,9526111548146945
0,5364920037091894; 0,9802982293456622
0,2824960556905731; 1,0233933805918003
0,23901855912948333; 1,0295416690471693
0,20091587084638962; 1,0219914477703118
0,17856844640353708; 1,003722373353608
"""

coords = []
for linha in dados_brutos.strip().split('\n'):
    if linha.strip():
        val_x, val_y = linha.split(';')
        coords.append((float(val_x.replace(',', '.')), float(val_y.replace(',', '.'))))
coords.append(coords[0]) 

xs_raw = np.array([p[0] for p in coords])
ys_raw = np.array([p[1] for p in coords])

dist_raw = np.zeros(len(xs_raw))
for i in range(1, len(xs_raw)):
    dist_raw[i] = dist_raw[i-1] + np.hypot(xs_raw[i]-xs_raw[i-1], ys_raw[i]-ys_raw[i-1])

num_pontos_simulacao = 500
sim_dist = np.linspace(0, dist_raw[-1], num_pontos_simulacao)
sim_x = np.interp(sim_dist, dist_raw, xs_raw)
sim_y = np.interp(sim_dist, dist_raw, ys_raw)

def smooth_periodic(arr, window):
    pad = np.concatenate((arr[-window:], arr, arr[:window]))
    res = np.convolve(pad, np.ones(window)/window, mode='same')
    return res[window:-window]

sim_x, sim_y = smooth_periodic(sim_x, 8), smooth_periodic(sim_y, 8)
sim_x[-1], sim_y[-1] = sim_x[0], sim_y[0] 
distancia_real_pista = 4309.0 
fisica_dist = (sim_dist / sim_dist[-1]) * distancia_real_pista

gaps_raw = np.diff(dist_raw)
gaps_raw = np.insert(gaps_raw, 0, gaps_raw[0])
sim_gaps = np.interp(sim_dist, dist_raw, gaps_raw)
densidade = 1.0 / (sim_gaps + 1e-6)
curv_norm = (densidade - densidade.min()) / (densidade.max() - densidade.min() + 1e-6)

mask_reta_principal = (fisica_dist > 3500) | (fisica_dist < 280)
mask_reta_oposta = (fisica_dist > 700) & (fisica_dist < 1150)
curv_norm = np.where(mask_reta_principal | mask_reta_oposta, 0, curv_norm)
curv_norm = np.where(curv_norm < 0.20, 0, curv_norm)
curv_norm = smooth_periodic(curv_norm, 12)
curv_norm = (curv_norm - curv_norm.min()) / (curv_norm.max() - curv_norm.min() + 1e-6)
curv_norm = np.roll(curv_norm, -10) 

v_limit_ms = (340 - 260 * curv_norm) / 3.6
dd = distancia_real_pista / num_pontos_simulacao
v_ms = np.copy(v_limit_ms)

for _ in range(3):
    for i in range(1, len(v_ms)):
        a_accel = max(0.5, 12.0 * (1 - (v_ms[i-1]/95.0)**1.5)) 
        v_ms[i] = min(v_ms[i], np.sqrt(v_ms[i-1]**2 + 2 * a_accel * dd))
    for i in range(len(v_ms)-2, -1, -1):
        v_ms[i] = min(v_ms[i], np.sqrt(v_ms[i+1]**2 + 2 * 45.0 * dd)) 
    v_ms[0] = min(v_ms[0], np.sqrt(v_ms[-1]**2 + 2 * 12.0 * dd))
    v_ms[-1] = min(v_ms[-1], np.sqrt(v_ms[0]**2 + 2 * 45.0 * dd))

v_base_fisica = v_ms * 3.6

clip_counter = 0
for i in range(1, len(v_base_fisica)):
    if v_base_fisica[i] > 325 and (v_base_fisica[i] - v_base_fisica[i-1]) < 0.8:
        clip_counter += 1
        v_base_fisica[i] -= clip_counter * 0.15
    else:
        clip_counter = 0

f_base_fisica = np.full(num_pontos_simulacao, 120.0)
for i in range(num_pontos_simulacao):
    prev_v = v_ms[i-1] if i > 0 else v_ms[-1]
    if prev_v > v_ms[i]:
        drop_energia = (prev_v**2 - v_ms[i]**2)
        f_base_fisica[i] = 120 + (drop_energia * 0.6)

f_base_fisica = smooth_periodic(f_base_fisica, 6)
f_base_fisica = np.roll(f_base_fisica, -5) 

# 2. ROTEIRO DA CORRIDA E INJEÇÃO DE "SUJEIRA" PARA ETL
num_voltas = 5
dados_totais = []

diretor_de_prova = {
    "MCL-Lando": { "vel": {1: 0.95, 2: 0.98, 3: 1.01, 4: 1.04, 5: 1.02}, "temp": {1: 0.90, 2: 0.95, 3: 1.00, 4: 1.06, 5: 1.01} },
    "MCL-Oscar": { "vel": {1: 0.99, 2: 1.01, 3: 0.82, 4: 0.94, 5: 0.95}, "temp": {1: 0.96, 2: 1.01, 3: 1.42, 4: 1.02, 5: 1.04} }
}

for piloto in ["MCL-Lando", "MCL-Oscar"]:
    tempo_acumulado = 0.0
    for volta in range(1, num_voltas + 1):
        m_vel = diretor_de_prova[piloto]["vel"][volta]
        m_tmp = diretor_de_prova[piloto]["temp"][volta]
        
        for p in range(num_pontos_simulacao):
            d_total = (volta - 1) * distancia_real_pista + fisica_dist[p]
            x, y = float(sim_x[p]), float(sim_y[p])
            vel = float(v_base_fisica[p]) * m_vel
            brk = float(f_base_fisica[p]) * m_tmp
            
            if volta == 1 and fisica_dist[p] < 400:
                vel = vel * ((fisica_dist[p] / 400.0) ** 0.6)
            
            # O Tempo Acumulado é imutável e baseado na física perfeita
            vel_ms = max(vel / 3.6, 2.0)
            tempo_acumulado += (distancia_real_pista / num_pontos_simulacao) / vel_ms
            
            # ---> INJEÇÃO DE SUJEIRA PARA A CAMADA PRATA LIMPAR <---
            vel_registro = vel
            brk_registro = brk
            
            # Simula falha de rádio (Nulos)
            if 600 < fisica_dist[p] < 700 and random.random() < 0.1:
                vel_registro = None
                
            # Simula erro de sensor (Outlier Extremo)
            if random.random() < 0.005:
                brk_registro = 9999.0

            dados_totais.append({
                "Piloto": piloto, "Volta": volta, "Distancia_Total": d_total, 
                "Track_X": x, "Track_Y": y, "Velocidade_KMH": vel_registro, 
                "Brake_Temp": brk_registro, "Tempo_Acumulado": tempo_acumulado
            })

df_raw = pd.DataFrame(dados_totais)

# Simula dados duplicados na rede
df_duplicados = df_raw.sample(n=100, random_state=42)
df_bronze_pd = pd.concat([df_raw, df_duplicados]).sort_index().reset_index(drop=True)

# Salvar no Spark
spark_df_bronze = spark.createDataFrame(df_bronze_pd)
spark_df_bronze.write.mode("overwrite").format("delta").saveAsTable("default.f1_telemetria_bronze")
print("✅ Camada BRONZE criada e salva (com sujeira injetada para teste)!")

# COMMAND ----------

from pyspark.sql import Window
import pyspark.sql.functions as F

bronze_df = spark.table("default.f1_telemetria_bronze")

# 1. Remover Linhas Duplicadas (Falhas de rede)
silver_df = bronze_df.dropDuplicates(["Piloto", "Volta", "Distancia_Total"])

# 2. Tratar Outliers de Sensor Termal (9999.0 vira a temperatura média segura de 120 graus)
silver_df = silver_df.withColumn(
    "Brake_Temp",
    F.when(F.col("Brake_Temp") >= 9999.0, 120.0).otherwise(F.col("Brake_Temp"))
)

# 3. Tratar Nulos de Velocidade usando o último dado válido (Forward Fill)
window_spec = Window.partitionBy("Piloto", "Volta").orderBy("Distancia_Total").rowsBetween(Window.unboundedPreceding, Window.currentRow)
silver_df = silver_df.withColumn("Velocidade_KMH", F.last("Velocidade_KMH", ignorenulls=True).over(window_spec))

# Salvar particionado por Piloto para otimizar leitura analítica
silver_df.write.mode("overwrite").partitionBy("Piloto").format("delta").saveAsTable("default.f1_telemetria_prata")
print("✅ Camada PRATA criada e salva (Nulos, Duplicatas e Outliers removidos)!")

# COMMAND ----------

import pyspark.sql.functions as F

prata_df = spark.table("default.f1_telemetria_prata")

# Aplica as regras de alerta de Engenharia Mecânica
ouro_df = prata_df.withColumn(
    "Alarme_Mecanico",
    F.when(F.col("Brake_Temp") >= 600.0, "🚨 CRÍTICO")
     .when(F.col("Brake_Temp") >= 400.0, "⚠️ ATENÇÃO")
     .otherwise("✅ ESTÁVEL")
)

ouro_df.write.mode("overwrite").format("delta").saveAsTable("default.f1_telemetria_ouro")
print("✅ Camada OURO criada e pronta para o Dashboard!")

# COMMAND ----------

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import base64
from IPython.display import display, HTML

# ==========================================
# 1. CONSUMO DA CAMADA OURO 
# ==========================================
print("⏳ Lendo dados da Camada Ouro...")
df_all = spark.table("default.f1_telemetria_ouro").toPandas()

# Garantir a ordem matemática após o processamento distribuído do Spark
df_all = df_all.sort_values(by=['Piloto', 'Volta', 'Tempo_Acumulado']).reset_index(drop=True)

df_l = df_all[df_all['Piloto'] == 'MCL-Lando'].copy().reset_index(drop=True)
df_o = df_all[df_all['Piloto'] == 'MCL-Oscar'].copy().reset_index(drop=True)

# Cálculo da Aceleração feito na camada de Visualização
for df_p in [df_l, df_o]:
    df_p['Aceleracao'] = ((df_p['Velocidade_KMH'] / 3.6).diff().fillna(0) / df_p['Tempo_Acumulado'].diff().fillna(1)).clip(-50, 20)

# Resgatando a geometria e constantes exatas a partir dos dados processados
tracado = df_l[df_l['Volta'] == 1]
sim_x = tracado['Track_X'].values
sim_y = tracado['Track_Y'].values
distancia_real_pista = 4309.0
num_voltas = 5

t_max_l = df_l.groupby("Volta")["Tempo_Acumulado"].max().to_dict()
t_max_o = df_o.groupby("Volta")["Tempo_Acumulado"].max().to_dict()
t_max_l[0], t_max_o[0] = 0.0, 0.0
t_v_l = {v: t_max_l[v] - t_max_l[v-1] for v in range(1, num_voltas + 1)}
t_v_o = {v: t_max_o[v] - t_max_o[v-1] for v in range(1, num_voltas + 1)}

# Reamostragem exata de 300 frames
num_frames = 300
tempos_globais = np.linspace(0, max(df_l['Tempo_Acumulado'].max(), df_o['Tempo_Acumulado'].max()), num_frames)

cols_interp = ['Track_X', 'Track_Y', 'Distancia_Total', 'Velocidade_KMH', 'Brake_Temp', 'Aceleracao', 'Volta']
anim_l = pd.DataFrame({col: np.interp(tempos_globais, df_l['Tempo_Acumulado'], df_l[col]) for col in cols_interp})
anim_o = pd.DataFrame({col: np.interp(tempos_globais, df_o['Tempo_Acumulado'], df_o[col]) for col in cols_interp})

# ==========================================
# 2. MONTAGEM DA INTERFACE E ANIMAÇÃO
# ==========================================
fig = make_subplots(rows=2, cols=1, subplot_titles=("Interlagos", "Telemetria Progressiva Escalonada"), vertical_spacing=0.20, row_heights=[0.55, 0.45])

fig.add_trace(go.Scatter(x=sim_x, y=sim_y, mode='lines', line=dict(color='#444444', width=6), showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=[sim_x[0]], y=[sim_y[0]], mode='text', text=['🏁'], textfont=dict(size=22), textposition='top right', showlegend=False), row=1, col=1)

fig.add_trace(go.Scatter(x=[anim_l['Distancia_Total'][0]], y=[anim_l['Velocidade_KMH'][0]], mode='lines', line=dict(color='#FF8000', width=2), name='Lando Norris', legend="legend2"), row=2, col=1)
fig.add_trace(go.Scatter(x=[anim_o['Distancia_Total'][0]], y=[anim_o['Velocidade_KMH'][0]], mode='lines', line=dict(color='#00BFFF', width=2), name='Oscar Piastri', legend="legend2"), row=2, col=1)

fig.add_trace(go.Scatter(x=[anim_l['Track_X'][0]], y=[anim_l['Track_Y'][0]], mode='markers', marker=dict(color='#FF8000', size=14, symbol='circle', line=dict(width=2, color='black')), showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=[anim_o['Track_X'][0]], y=[anim_o['Track_Y'][0]], mode='markers', marker=dict(color='#00BFFF', size=14, symbol='circle', line=dict(width=2, color='black')), showlegend=False), row=1, col=1)

x_min, x_max = min(sim_x), max(sim_x)
y_min, y_max = min(sim_y), max(sim_y)

fig.add_trace(go.Scatter(x=[x_max*1.15, x_max*1.15], y=[y_max*0.7, y_max*0.3], mode='text', text=["", ""], textfont=dict(size=14, color=["#FF8000", "#00BFFF"]), textposition="middle right", showlegend=False), row=1, col=1)
fig.add_trace(go.Scatter(x=[distancia_real_pista*1.5, distancia_real_pista*3.5], y=[480, 480], mode='text', text=["", ""], textfont=dict(size=13, color=["#FF8000", "#00BFFF"]), textposition="top center", showlegend=False), row=2, col=1)

for v in range(1, num_voltas):
    fig.add_shape(type="line", x0=v*distancia_real_pista, x1=v*distancia_real_pista, y0=0, y1=590, line=dict(color="lightgray", width=1, dash="dot"), row=2, col=1)

frames = []
for i in range(num_frames):
    v_l, v_o = int(anim_l['Volta'][i]), int(anim_o['Volta'][i])
    lap_txt_l = f"{t_v_l[v_l-1]:.2f}s" if v_l > 1 else "--"
    lap_txt_o = f"{t_v_o[v_o-1]:.2f}s" if v_o > 1 else "--"

    # ---> CORREÇÃO: Traduzindo a temperatura no frame atual para refletir o status da Camada Ouro <---
    alarme_l = "🚨 CRÍTICO" if anim_l['Brake_Temp'][i] >= 600 else ("⚠️ ATENÇÃO" if anim_l['Brake_Temp'][i] >= 400 else "✅ ESTÁVEL")
    alarme_o = "🚨 CRÍTICO" if anim_o['Brake_Temp'][i] >= 600 else ("⚠️ ATENÇÃO" if anim_o['Brake_Temp'][i] >= 400 else "✅ ESTÁVEL")

    frames.append(go.Frame(
        data=[
            go.Scatter(x=anim_l['Distancia_Total'][:i+1], y=anim_l['Velocidade_KMH'][:i+1]), 
            go.Scatter(x=anim_o['Distancia_Total'][:i+1], y=anim_o['Velocidade_KMH'][:i+1]), 
            go.Scatter(x=[anim_l['Track_X'][i]], y=[anim_l['Track_Y'][i]]),                  
            go.Scatter(x=[anim_o['Track_X'][i]], y=[anim_o['Track_Y'][i]]),                  
            go.Scatter(text=[
                f"<b>NORRIS</b><br>Freio: {anim_l['Brake_Temp'][i]:.0f}°C<br>Status: {alarme_l}<br>Últ. Volta: {lap_txt_l}", 
                f"<b>PIASTRI</b><br>Freio: {anim_o['Brake_Temp'][i]:.0f}°C<br>Status: {alarme_o}<br>Últ. Volta: {lap_txt_o}"
            ]), 
            go.Scatter(text=[f"<b>NORRIS</b><br>Vel: {anim_l['Velocidade_KMH'][i]:.0f} km/h | Acel: {anim_l['Aceleracao'][i]:.1f} m/s²", f"<b>PIASTRI</b><br>Vel: {anim_o['Velocidade_KMH'][i]:.0f} km/h | Acel: {anim_o['Aceleracao'][i]:.1f} m/s²"]) 
        ], traces=[2, 3, 4, 5, 6, 7], name=f"f{i}")) 
fig.frames = frames

m_x, m_y = (x_max - x_min) * 0.15, (y_max - y_min) * 0.15

fig.update_layout(
    paper_bgcolor="white", plot_bgcolor="white", font=dict(color="black"), height=950, margin=dict(t=80, b=150, l=80, r=40),
    legend2=dict(title="", orientation="h", y=0.46, x=0.5, xanchor="center", yanchor="top", bgcolor="rgba(255,255,255,0.8)"),
    updatemenus=[{"type": "buttons", "direction": "down", "x": -0.08, "xanchor": "left", "y": -0.15, "bgcolor": "#E0E0E0", "buttons": [
        {"label": "▶ LIVE STREAM", "method": "animate", "args": [None, {"frame": {"duration": 150, "redraw": False}, "fromcurrent": True}]},
        {"label": "⏸ PAUSE", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]}
    ]}],
    sliders=[{"active": 0, "x": 0.08, "xanchor": "left", "y": -0.15, "len": 0.92, "currentvalue": {"prefix": "Tempo: "}, "steps": [{"args": [[f"f{i}"], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}], "label": f"{t:.1f}s", "method": "animate"} for i, t in enumerate(tempos_globais)]}]
)

fig.update_xaxes(range=[x_min - m_x, x_max + m_x*3], showgrid=False, zeroline=False, showticklabels=False, row=1, col=1) 
fig.update_yaxes(range=[y_min - m_y, y_max + m_y], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, showticklabels=False, row=1, col=1)
fig.update_xaxes(range=[0, distancia_real_pista * num_voltas], title="Distância Acumulada da Sprint Race (m)", showgrid=True, gridcolor="#EEEEEE", row=2, col=1)
fig.update_yaxes(range=[0, 600], title="Velocidade (Km/h)", showgrid=True, gridcolor="#EEEEEE", row=2, col=1)

html_content = fig.to_html(auto_play=False)
b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')

display(HTML(f'''
<div style="margin-top: 20px; padding: 20px; background-color: #e8f5e9; border: 2px solid #4caf50; border-radius: 8px; text-align: center;">
    <h2 style="color: #2e7d32; margin-top: 0; margin-bottom: 5px; font-family: sans-serif;">🏆 GÊMEO DIGITAL DE INTERLAGOS (GOLD LAYER)</h2>
    <p style="font-size: 16px; margin-top: 5px; font-family: sans-serif;">Pipeline completo executado com sucesso!</p>
    <br>
    <a download="f1_interlagos_master_final.html" href="data:text/html;base64,{b64}" 
       style="font-size: 18px; font-weight: bold; background-color: #FF8000; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); font-family: sans-serif; display: inline-block;">
       📥 BAIXAR O PROJETO FINAL
    </a>
</div>
'''))
displayHTML(fig.to_html(include_plotlyjs='cdn'))