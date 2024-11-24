rm caie_gerar_grafico.zip

rm -r caie_gerar_grafico/*

cp extract_data.py caie_gerar_grafico/
cp executar.bat caie_gerar_grafico/

cp -r grafico_grandao/ caie_gerar_grafico/
cp -r grafico_linha_estoques/ caie_gerar_grafico/
cp -r grafico_timeline_produtos_relacionados/ caie_gerar_grafico/

zip -r caie_gerar_grafico.zip caie_gerar_grafico/