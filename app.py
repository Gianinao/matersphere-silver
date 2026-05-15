import streamlit as st
import pandas as pd
from textblob import TextBlob

# ============================================================
# MaterSphere Silver — MVP Streamlit
# Sistema inteligente de pré-consulta com IA empática
# ============================================================

st.set_page_config(
    page_title="MaterSphere Silver",
    page_icon="🩶",
    layout="wide"
)

palavras_risco = [
    "não vou", "acho que não", "inseguro", "insegura",
    "dor", "cansado", "cansada", "difícil", "longe", "esqueci",
    "preocupado", "preocupada", "medo", "ansioso", "ansiosa",
    "não consigo", "não sei", "talvez não"
]

def analisar_sentimento(texto):
    if not texto or texto.strip() == "":
        return 0.0, "neutro"

    blob = TextBlob(texto)
    score = blob.sentiment.polarity

    if score > 0.1:
        label = "positivo"
    elif score < -0.1:
        label = "negativo"
    else:
        label = "neutro"

    return score, label

def detectar_palavras(texto):
    if not texto:
        return []
    texto_lower = texto.lower()
    return [palavra for palavra in palavras_risco if palavra in texto_lower]

def calcular_risco(sentimento_score, idade, faltas_anteriores, dias_ate_consulta, palavras_detectadas):
    risco = 0

    if sentimento_score < -0.3:
        risco += 30
    if idade >= 60:
        risco += 15
    if faltas_anteriores >= 2:
        risco += 25
    if dias_ate_consulta <= 1:
        risco += 15
    if len(palavras_detectadas) > 0:
        risco += 20

    return min(risco, 100)

def classificar_risco(score):
    if score >= 70:
        return "ALTO"
    elif score >= 40:
        return "MÉDIO"
    else:
        return "BAIXO"

def definir_acao(classificacao):
    if classificacao == "ALTO":
        return "Alertar familiar e oferecer apoio humano"
    elif classificacao == "MÉDIO":
        return "Reforçar lembrete e confirmar presença"
    else:
        return "Enviar lembrete padrão"

st.markdown(
    """
    <style>
        .main {
            background-color: #F7F9FA;
        }

        .header-box {
            background: linear-gradient(135deg, #8FB6FF 0%, #AEE1CD 100%);
            padding: 30px;
            border-radius: 24px;
            margin-bottom: 24px;
            box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.08);
        }

        .header-title {
            color: #12324A;
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .header-subtitle {
            color: #24485C;
            font-size: 20px;
            margin-top: 0px;
        }

        .info-card {
            background-color: white;
            padding: 22px;
            border-radius: 20px;
            box-shadow: 0px 4px 18px rgba(0,0,0,0.06);
            margin-bottom: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="header-box">
        <div class="header-title">MaterSphere Silver</div>
        <div class="header-subtitle">
            Sistema inteligente de pré-consulta com IA empática
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    "Este MVP simula uma camada inteligente de pré-consulta. "
    "A partir da mensagem do paciente, o sistema analisa sinais emocionais, "
    "calcula o risco de não comparecimento e sugere uma ação preventiva."
)

col1, col2 = st.columns([1.15, 1])

with col1:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Entrada do paciente")

    mensagem = st.text_area(
        "Como você está se sentindo hoje?",
        placeholder="Exemplo: Estou meio insegura, acho que não vou conseguir ir amanhã",
        height=120
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        idade = st.number_input("Idade", min_value=0, max_value=120, value=74)

    with c2:
        faltas_anteriores = st.number_input("Faltas anteriores", min_value=0, max_value=20, value=1)

    with c3:
        dias_ate_consulta = st.number_input("Dias até a consulta", min_value=0, max_value=365, value=1)

    analisar = st.button("Analisar paciente", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.subheader("Resultado da análise")

    if analisar:
        sentimento_score, sentimento_label = analisar_sentimento(mensagem)
        palavras = detectar_palavras(mensagem)

        score_risco = calcular_risco(
            sentimento_score,
            idade,
            faltas_anteriores,
            dias_ate_consulta,
            palavras
        )

        classificacao = classificar_risco(score_risco)
        acao = definir_acao(classificacao)

        st.metric("Score de risco", f"{score_risco}/100")

        if classificacao == "ALTO":
            st.error(f"Classificação: {classificacao}")
        elif classificacao == "MÉDIO":
            st.warning(f"Classificação: {classificacao}")
        else:
            st.success(f"Classificação: {classificacao}")

        st.write(f"**Sentimento detectado:** {sentimento_label}")
        st.write(f"**Score emocional:** {sentimento_score:.2f}")

        if palavras:
            st.write(f"**Palavras de risco detectadas:** {', '.join(palavras)}")
        else:
            st.write("**Palavras de risco detectadas:** nenhuma")

        st.write(f"**Ação sugerida:** {acao}")

        resultado = pd.DataFrame([{
            "mensagem_chat": mensagem,
            "idade": idade,
            "faltas_anteriores": faltas_anteriores,
            "dias_ate_consulta": dias_ate_consulta,
            "sentimento_score": sentimento_score,
            "sentimento_label": sentimento_label,
            "palavras_detectadas": ", ".join(palavras),
            "score_risco": score_risco,
            "classificacao_risco": classificacao,
            "acao_final": acao
        }])

        st.session_state["resultado"] = resultado

    else:
        st.info("Preencha os dados do paciente e clique em analisar.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="info-card">', unsafe_allow_html=True)
st.subheader("Registro da interação")

if "resultado" in st.session_state:
    resultado_df = st.session_state["resultado"]
    st.dataframe(resultado_df, use_container_width=True)

    csv = resultado_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "Baixar resultado em CSV",
        data=csv,
        file_name="resultado_matersphere_silver.csv",
        mime="text/csv"
    )
else:
    st.write("Nenhuma análise realizada ainda.")

st.markdown('</div>', unsafe_allow_html=True)

st.caption(
    "MVP acadêmico desenvolvido para demonstrar o conceito de IA empática aplicada à pré-consulta hospitalar."
)