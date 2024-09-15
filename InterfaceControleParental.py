import flet as ft
import matplotlib.pyplot as plt
import io
import base64
import matplotlib  # Importando matplotlib

# Definindo o backend para evitar erros relacionados ao loop principal
matplotlib.use('Agg')

def main(page: ft.Page):

    # Configurações iniciais da página
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 1200
    page.window_height =775
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.BLUE,
            primary_container=ft.colors.BLUE_200
        ),
    )
    # Título do Programa
    title = ft.Text("Nome do Programa", size=30, weight=ft.FontWeight.BOLD)

    # Função para trocar de aba
    def change_tab(e):
        # Oculta todos os conteúdos das abas
        for idx, content in enumerate(tab_contents):
            content.visible = False
        # Exibe o conteúdo da aba selecionada
        tab_contents[int(e.control.selected_index)].visible = True
        page.update()

    # Barra de itens com ícones e texto
    tab_bar = ft.Tabs(
        tabs=[
            ft.Tab(text="Gerenciar Aplicativos", icon=ft.icons.DEVICE_HUB),
            ft.Tab(text="Gerenciar Sites", icon=ft.icons.PUBLIC),
        ],
        on_change=change_tab
    )

    # Dados iniciais para a tabela de aplicativos
    apps_data = [
        ["YouTube", "2 horas"],
        ["Facebook", "1.5 horas"],
        ["Instagram", "1 hora"],
        ["TikTok", "0.5 horas"]
    ]

    # Função para gerar o gráfico de barras personalizado
    def generate_bar_chart():
        app_names = [app[0] for app in apps_data]
        usage_times = [float(app[1].split()[0]) for app in apps_data]

        # Configuração do gráfico
        plt.figure(figsize=(5, 3), facecolor='none')
        plt.bar(app_names, usage_times, color='#2196f3')

        # Personalizações
        plt.xlabel('Aplicativo', color='white')
        plt.ylabel('Tempo de Uso (horas)', color='white')
        plt.title('Tempo de Uso por Aplicativo', color='white')

        plt.tight_layout()
        
        # Alterando a cor dos rótulos e ticks dos eixos
        plt.gca().spines['bottom'].set_color('grey')  # Cor da borda inferior
        plt.gca().spines['left'].set_color('grey')    # Cor da borda esquerda
        plt.gca().spines['right'].set_color('none')    # Cor da borda direita
        plt.gca().spines['top'].set_color('none')    # Cor da borda topo
        plt.gca().xaxis.label.set_color('white')       # Cor do rótulo do eixo X
        plt.gca().yaxis.label.set_color('white')       # Cor do rótulo do eixo Y
        plt.gca().tick_params(colors='white')          # Cor dos ticks

        # Fundo transparente
        plt.gca().set_facecolor('none')  # Define fundo transparente no gráfico
        plt.grid(False)  # Remove a grade para mais clareza

        # Salva o gráfico em um buffer de memória com fundo transparente
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        plt.close()

        # Codifica a imagem em base64
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return img_base64

    # Função para atualizar o gráfico
    def update_chart():
        chart_image.src_base64 = generate_bar_chart()
        page.update()

    # Campos de entrada para nome e tempo de uso do aplicativo
    new_app_name = ft.TextField(label="Nome do Aplicativo", width=300)
    new_app_time = ft.TextField(label="Tempo", width=300)
    add_app_btn = ft.ElevatedButton("Defina o Tempo de Uso")

    # Função para gerar a tabela de aplicativos
    def generate_app_table():
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Aplicativo")),
                ft.DataColumn(ft.Text("Tempo de Uso")),
            ],
            rows=[ft.DataRow(
                cells=[ft.DataCell(ft.Text(app[0])), ft.DataCell(ft.Text(app[1]))])
                for app in apps_data],
                width=500
        )

    # Função para adicionar um aplicativo à tabela e atualizar o gráfico
    def add_app(e):
        app_name = new_app_name.value
        app_time = new_app_time.value
        if app_name and app_time:
            apps_data.append([app_name, app_time])
            app_table.controls.clear()
            app_table.controls.append(generate_app_table())
            update_chart()
            new_app_name.value = ""
            new_app_time.value = ""
            page.update()

    add_app_btn.on_click = add_app

    # Criação da tabela de aplicativos
    app_table = ft.Column([generate_app_table()])

    # Gráfico de barras (inicial)
    chart_image = ft.Image(src_base64=generate_bar_chart(), width=500, height=300)

    # Layout horizontal para os campos de entrada e tabela de aplicativos
    app_content = ft.Column([
        ft.Row([
            ft.Column([
            ft.Text("Gerenciar Aplicativos", size=20, weight=ft.FontWeight.W_600),
            ft.Column([chart_image], alignment=ft.MainAxisAlignment.START),
            ft.Column([app_table], alignment=ft.MainAxisAlignment.START)
            ], alignment=ft.MainAxisAlignment.START),
            ft.VerticalDivider(),  # Divisor vertical entre campos e tabela
            ft.Column([
            ft.Text("Definir Tempo de App", size=20, weight=ft.FontWeight.W_600),
            new_app_name,
            new_app_time,
            add_app_btn,
            ft.VerticalDivider(),
            ], alignment=ft.MainAxisAlignment.START),
        ], expand=True)
    ], visible=True)

    # Campos de entrada para aba sites
    inserir_site = ft.TextField(label="Adicionar site", width=300)
    bloquear_site = ft.ElevatedButton("Bloquear Site")

    # Dados iniciais para a tabela de sites
    sites_data = [
        ["www.youtube.com"],
        ["www.facebook.com"],
        ["www.instagram.com"],
        ["www.tiktok.com"]
    ]

    # Função para gerar a tabela de sites
    def generate_sites_table():
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Sites Bloqueados")),
            ],
            rows=[ft.DataRow(
                cells=[ft.DataCell(ft.Text(site[0]))])
                for site in sites_data]
        )

    # Criação da tabela de sites
    sites_table = ft.Column([generate_sites_table()])

    # Layout horizontal para os campos de entrada e tabela de sites
    sites_content = ft.Column([
        ft.Text("Gerenciar Sites", size=20, weight=ft.FontWeight.W_600),
        ft.Row([
            ft.Column([
                inserir_site,
                bloquear_site
            ], alignment=ft.MainAxisAlignment.START),
            ft.VerticalDivider(),  # Divisor vertical entre campos e tabela
            ft.Column([sites_table], alignment=ft.MainAxisAlignment.START),
            ft.VerticalDivider(),
        ], expand=True)
    ], visible=False)

    # Lista de conteúdos das abas para facilitar a troca
    tab_contents = [app_content, sites_content, ]

    # Usando Stack para empilhar os conteúdos das abas, de modo que apenas um seja visível por vez
    content_stack = ft.Stack(controls=tab_contents, expand=True)

    # Adicionando todos os elementos à página
    page.add(
        title,
        tab_bar,
        content_stack
    )

# Iniciar o aplicativo
ft.app(target=main)
