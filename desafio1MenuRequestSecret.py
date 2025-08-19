import string
import urllib.request
import ssl
import socket

# Configurações de SSL
ssl._create_default_https_context = ssl._create_unverified_context
socket.setdefaulttimeout(8)

valid_urls = []
url_base_pattern = ""

def verificar_urls_reais(pattern, num_urls=5):
    letras = string.ascii_lowercase
    resultados = []
    
    for i in range(num_urls):
        sufixo = ''.join([letras[(i // (26**j)) % 26] for j in reversed(range(3))])
        url = pattern.replace("*", sufixo)
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'text/html',
                'Accept-Language': 'pt-BR,pt;q=0.9'
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req) as response:
                status_code = response.status
                content_type = response.headers.get('Content-Type', '')
                
                if 'text/html' not in content_type:
                    resultados.append({
                        "url": url,
                        "status": status_code,
                        "html_content": f"Conteúdo não HTML: {content_type}",
                        "headers": dict(response.headers),
                        "status_kryptos": "❌"
                    })
                    continue
                
                html_content = response.read().decode('utf-8', errors='replace')[:1000]
                
                is_valid_page = True
                if any(palavra in html_content.lower() for palavra in ['404', 'não encontrada', 'error']):
                    is_valid_page = False
                
                resultados.append({
                    "url": url,
                    "status": status_code,
                    "html_content": html_content,
                    "headers": dict(response.headers),
                    "status_kryptos": "✅" if is_valid_page else "❌"
                })
                
        except urllib.error.HTTPError as e:
            resultados.append({
                "url": url,
                "status": e.code,
                "html_content": f"Erro HTTP: {e.reason}",
                "headers": {},
                "status_kryptos": "❌"
            })
        except Exception as e:
            resultados.append({
                "url": url,
                "status": 500,
                "html_content": f"Erro: {str(e)}",
                "headers": {},
                "status_kryptos": "❌"
            })
    
    return resultados

def exibir_resultados():
    if not valid_urls:
        print("Nenhuma URL verificada ainda.")
        return
    
    print("\nResultado das páginas encontradas:")
    for i, item in enumerate(valid_urls, 1):
        tick = item['status_kryptos']
        print(f"{i}. {item['url']} - Status HTTP: {item['status']} - {tick}")
        print(f"   HTML: {item['html_content']}")
        if 'decrypted_text' in item:
            print(f"   Decrypted: {item['decrypted_text']}")
    
    print(f"\nTotal: {len(valid_urls)} páginas armazenadas.")

def mostrar_lista_completa():
    """if not valid_urls:
        print("Nenhuma URL verificada ainda.")
        return"""
    
    print("\nLista completa de dicionários:")
    for i, item in enumerate(valid_urls, 1):
        print(f"\nItem {i}:")
        print(f"  URL: {item['url']}")
        print(f"  Status: {item['status']}")
        print(f"  Kryptos: {item['status_kryptos']}")
        print("  Headers:")
        for key, value in item['headers'].items():
            print(f"    {key}: {value}")
        print(f"  HTML Content: {item['html_content'][:200]}...")  # Mostra apenas o início do conteúdo
        if 'decrypted_text' in item:
            print(f"  Decrypted: {item['decrypted_text']}")
    
    print(f"\nTotal: {len(valid_urls)} registros.")

def marcar_manual():
    exibir_resultados()
    try:
        idx = int(input("Digite o número da URL para marcar: ")) - 1
        if 0 <= idx < len(valid_urls):
            novo = input("Digite 1-✅ para válida ou 2-❌ para inválida: ").strip()
            if novo == "1":
                valid_urls[idx]['status_kryptos'] = "✅"
            elif novo == "2":
                valid_urls[idx]['status_kryptos'] = "❌"
            else:
                print("Entrada inválida. Use 1 ou 2.")
        else:
            print("Índice fora do intervalo.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

def deletar_entrada():
    exibir_resultados()
    try:
        idx = int(input("Digite o número da URL a ser deletada: ")) - 1
        if 0 <= idx < len(valid_urls):
            del valid_urls[idx]
            print("Removido com sucesso.")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

def limpar_falsos():
    global valid_urls
    antes = len(valid_urls)
    valid_urls = [v for v in valid_urls if v['status_kryptos'] == '✅']
    print(f"Removidos {antes - len(valid_urls)} registros com ❌.")

def decriptar_kryptos():
    for v in valid_urls:
        if v['status_kryptos'] == '✅' and 'decrypted_text' not in v:
            texto = v['headers'].get('kryptos', '')
            v['decrypted_text'] = decodeROT13(texto)
    print("Todos os textos 'kryptos' foram decriptados.")

def verificar_conexao():
    try:
        urllib.request.urlopen('http://google.com', timeout=5)
        return True
    except:
        return False

def menu():
    global url_base_pattern, valid_urls
    
    while True:
        print("\nMenu:")
        print("1. Definir base da URL com wildcard (*)")
        print("2. Verificar e exibir páginas HTML")
        print("3. Marcar manualmente uma URL")
        print("4. Deletar um registro específico")
        print("5. Limpar registros inválidos")
        print("6. Decriptar textos kryptos")
        print("7. Mostrar lista completa de dicionários")
        print("8. Sair")
        
        op = input("Digite o número da opção: ").strip()
        
        if op == "1":
            url_base_pattern = input("Digite a base da URL com * (ex: https://*.site.com): ").strip()
        elif op == "2":
            if not url_base_pattern:
                print("⚠️ Defina primeiro a base da URL (opção 1).")
            else:
                if verificar_conexao():
                    valid_urls = verificar_urls_reais(url_base_pattern)
                    exibir_resultados()
                else:
                    print("⚠️ Sem conexão com a internet. Verifique sua rede.")
        elif op == "3":
            if valid_urls:
                marcar_manual()
            else:
                print("⚠️ Nenhuma URL disponível. Verifique URLs primeiro (opção 2).")
        elif op == "4":
            if valid_urls:
                deletar_entrada()
            else:
                print("⚠️ Nenhuma URL para deletar.")
        elif op == "5":
            limpar_falsos()
        elif op == "6":
            if any(v['status_kryptos'] == '✅' for v in valid_urls):
                decriptar_kryptos()
                exibir_resultados()
            else:
                print("⚠️ Nenhum registro válido para decriptar.")
        elif op == "7":
            mostrar_lista_completa()
        elif op == "8":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    print("="*50)
    print("Scanner Web - Requisições Reais")
    print("="*50)
    if not verificar_conexao():
        print("AVISO: Sem conexão com a internet. Algumas funcionalidades podem falhar.")
    menu()