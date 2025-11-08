% ================= Motor de inferencia simple ==================
% Hechos esperados en el entorno:
%  - tiene(Animal, Atributo).
%  - regla(Label, [Cond1, Cond2, ...]).  donde Condi son literales Prolog
%
% Uso principal:
%   clasifica(Animal, Label).
%
% También puedes pedir explicación:
%   explica(Animal, Label, CondsCumplidas).

cumple(_, []) :- !.
cumple(X, [C|Cs]) :-
    call(C, X),
    !,
    cumple(X, Cs).

clasifica(Animal, Label) :-
    regla(Label, Conds),
    cumple(Animal, Conds),
    !.

% Explicación básica: devuelve las condiciones de la primera regla que se cumpla
explica(Animal, Label, Conds) :-
    regla(Label, Conds),
    cumple(Animal, Conds),
    !.
