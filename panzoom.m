function panzoom(src,evt)
% Funktion, um Achsen greifen zu können, und hin und her zu ziehen, sowie mit dem Mausrad zu zoomen.
% INPUT: Source und Event des Callbacks (s. Callback Functions)
%
% Version: 1.0
% Datum: 2017-04-06
% Autor: Peter Jüstel
% Lizenz: CC-BY-SA 4.0 (Feel free, but attribute the author, and share remixes under similar terms)
% https://creativecommons.org/licenses/by-sa/4.0/
% https://creativecommons.org/licenses/by-sa/4.0/legalcode
%
% Implementierhinweise: Die Funktion muss als Callback der Figure und der Achse eingerichtet werden. Entweder direkt für die WindowButtonMotionFcn', 'WindowButtonUpFcn','WindowScrollWheelFcn' der Figure, und der 'ButtonDownFcn' der Achse. Oder aufgerufen innerhalb der entsprechenden Callback functions, falls die Callbacks noch andere Dinge können sollen. Funktionsfile evtl. in subordner mit addpath sichtbar machen.
% Vorsicht: guidata der figure muss ein Struct array sein, falls es genutzt wird. 
%
% --> Shut up, and take my panzoom!!
% allfigures = findall(0, 'type','figure');
% allaxes = findall(0, 'type', 'axes');
% for ii = 1:size(allfigures, 1)
%     allfigures(ii).WindowButtonMotionFcn = @panzoom;
%     allfigures(ii).WindowButtonUpFcn = @panzoom;
%     allfigures(ii).WindowScrollWheelFcn = @panzoom;
% 	  allfigures(ii).WindowKeyPressFcn = @panzoom;
% 	  allfigures(ii).WindowKeyReleaseFcn = @panzoom;
% end
% for ii = 1:size(allaxes,1)
%     allaxes(ii).ButtonDownFcn = @panzoom;
% end

%%%% TODO
%


%%%% Initialisieren der Vars
fenster = guidata(src);			% flags und daten aus der figure auslesen (guidata(axis) leitet auf die beinhaltende figure weiter).
if isempty(fenster)				% Wenn das Fenster noch keine Flags/Daten gespeichert hat -> initialisieren.
	fenster.pannerflag = 0;		% flag setzen, die das verschieben der Achsen erlaubt.
	fenster.xzoom = 1;			% flag setzen, die bestimmt, ob nur auf der x-achse gezoomt werden soll (default = ja). D.h. die y-achse wird festgehalten.
	fenster.yzoom = 1;			% flag; selbe wie xzoom, nur für die y-achse.
	fenster.oldpoint = [0 0];	% aktuellen Punkt initialisieren.
end



%%%% Pan

if strcmp(evt.EventName, 'Hit') && src == gca	% wird ausgelöst beim clicken irgenwo innerhalb der Achse
	fenster.pannerflag = 1;						% flag setzen, die das verschieben der achsen erlaubt.
	fenster.oldpoint = src.CurrentPoint(1,1:2);		% aktuellen Punkt merken
	guidata(src, fenster)	% flags und daten speichern.
	
elseif strcmp(evt.EventName, 'WindowMouseRelease')	% wird ausgelöst, wenn die Maustaste wieder losgelassen wird.
	fenster.pannerflag = 0;
	guidata(src, fenster)	% flags und daten speichern.

end

if strcmp(evt.EventName, 'WindowMouseMotion')	% wird ausgelöst, wenn die Maus innerhalb des Fensters bewegt wird.
	if fenster.pannerflag == 1
		Achse1 = evt.Source.CurrentAxes;

		C = Achse1.CurrentPoint(1,1:2);
		Achse1.XLim = Achse1.XLim + (fenster.oldpoint(1) - C(1));	% verschiebe die Achsengrenzen/Ansicht so, dass der Punkt der Maus folgt.
		Achse1.YLim = Achse1.YLim + (fenster.oldpoint(2) - C(2));
	end
end



%%%% Zoomen

% Trigger
if strcmp(evt.EventName, 'WindowKeyPress')
	if strcmp(evt.Key, 'control')		% deaktivert zoomen in x-richtung -> Y-zoom
		fenster.xzoom = 0;
		guidata(src, fenster)	% flag speichern.
	elseif strcmp(evt.Key, 'shift')
		fenster.yzoom = 0;			% deaktivert zoomen in y-richtung -> X-zoom
		guidata(src, fenster)
	end
elseif strcmp(evt.EventName, 'WindowKeyRelease')
	if strcmp(evt.Key, 'control')
		fenster.xzoom = 1;
		guidata(src, fenster)
	elseif strcmp(evt.Key, 'shift')
		fenster.yzoom = 1;
		guidata(src, fenster)
	end
end
	
% Action
if strcmp(evt.EventName, 'WindowScrollWheel')	% Wird ausgelöst, wenn das Scrollrad gedreht wird.
	Achse1 = evt.Source.CurrentAxes;
	if evt.VerticalScrollCount < 0
		zoomfaktor = 1/1.3;		% reinzoomen
	else
		zoomfaktor = 1.3;		% rauszoomen
	end
	if fenster.xzoom == 1
		Achse1.XLim = zoomfaktor*Achse1.XLim + (1-zoomfaktor)*Achse1.CurrentPoint(1,1); % Auf der x-Achse soll nur gezoomt werden, wenn shift NICHT gedrückt ist.
	end
	if fenster.yzoom == 1
		Achse1.YLim = zoomfaktor*Achse1.YLim + (1-zoomfaktor)*Achse1.CurrentPoint(1,2);
	end
end


end

%%%% Notizen


% guidata(figure_handle, Variable) -> speichern
% data = guidata(figure_handle)		-> laden


% Durch src kann ich herausfinden, auf was geklickt wurde.
% evt.EventName = WindowMouseMotion
% evt.EventName = WindowMouseRelease
% evt.EventName = Hit, evt.Button = 1, evt.IntersectionPoint = [x y]?
% evt.Source = Axes/figure, vergleich mit gcf, gca?
% evt.Source.CurrentPoint = [x y] (vermutlich)
%

% get all the handles!
% allAxesInFigure = findall(figureHandle,'type','axes');
% If you want to get all axes handles anywhere in Matlab, you could do the following:
% allAxes = findall(0,'type','axes');