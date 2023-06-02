clear all
close all

% Importa i dati dal foglio di lavoro
tempi = load("matlab.mat", "tabellatempi");

% Manipolazione dei dati
A = tempi.tabellatempi; % Carica i dati nella variabile A
B = table2array(A); % Converte la tabella in un array
T = str2double(B); % Converte gli elementi dell'array in numeri

% Rimuove la riga 20 dalla matrice T
T(20,:) = [];

% Estrae i dati delle due popolazioni da T
P1 = T(:,1); % (Anna)
P2 = T(:,2); % (Andrea)

% Calcola la media delle due popolazioni
m1 = mean(P1);
m2 = mean(P2);

N = length(T); % Numero di elementi nel vettore T

% Crea un vettore x che va da 1 a N
for i = 1:N
    x(i) = i;
end
    
% Calcola la deviazione standard delle due popolazioni
err1 = std(P1);
err2 = std(P2);

% Crea i vettori y1 e y2, che contengono la media corrispondente
% per ogni elemento dix 
for i = 1:N
    y1(i) = m1;
    y2(i) = m2;
end


% Calcola il t-test con i dati importati

[h, p, ci, stats] = ttest(P1, P2, 'Alpha', 0.05);

% Visualizza i risultati del t-test
disp(['Valore t: ', num2str(stats.tstat)]);
disp(['P-value: ', num2str(p)]);
disp(['Intervallo di confidenza: [', num2str(ci(1)), ', ', num2str(ci(2)), ']']);
if h
    disp('I tempi di esecuzione sono significativamente diversi.');
else
    disp('Non ci sono differenze significative tra i tempi di esecuzione.');
end
