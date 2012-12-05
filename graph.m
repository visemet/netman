    
files = dir(fullfile('datafiles', '*.dta'))
for i = 1:size(files)
    filename = strcat('datafiles/',files(i).name)
    s = dir(filename)
    if s.bytes ~= 0
        M = dlmread(filename, '\t')
        plot(M(:,1), M(:,2), '.-')
        newname = strrep(filename, 'datafiles', 'graphs')
        newname = strrep(newname, 'dta', 'png')
        saveas(gcf, newname)
    end
    
end

graph_types = char('bufferoccupancy', 'linkrate', 'windowsize', 'flowrate')
for j = 1:size(graph_types)
    currgraph = strcat(graph_types(j), '*.dta')
    files = dir(fullfile('datafiles', currgraph))
    colors = char('r', 'b', 'g');
    for i = 1:size(files)
        filename = strcat('datafiles/',files(i).name)
        s = dir(filename);
        if s.bytes ~= 0
            M = dlmread(filename, '\t');
            color = strcat('.-', colors(i));
            p = plot(M(:,1), M(:,2), color);
            %hold off
            if i == 1
                legend(files(i).name);
            end
            if i > 1
                [LEGH, OBJH, OUTH, OUTM] = legend;
                legend([OUTH;p],OUTM{:}, files(i).name);
            end
            hold on
        end   
    end
    newname = strcat(graph_types(j), '_total', 'png');
    newname = strcat('total_graphs/', newname)
    %saveas(gcf, newname)
    print(gcf, '-r80', '-dpng', newname);
    clf
end