package org.example;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class Replace {
    public static String dsPy = "../../simnet/utils/ds.py";
    public static String versionRe = "MIYOUSHE_VERSION = \"(.*?)\"";
    public static String appDsRe = "MIYOUSHE_APP_DS = \"(.*?)\"";
    public static String webDsRe = "MIYOUSHE_WEB_DS = \"(.*?)\"";

    public static String replaceVersion(String line, String version) {
        return line.replaceAll(versionRe, "MIYOUSHE_VERSION = \"" + version + "\"");
    }

    public static String replaceAppDs(String line, String appDs) {
        return line.replaceAll(appDsRe, "MIYOUSHE_APP_DS = \"" + appDs + "\"");
    }

    public static String replaceWebDs(String line, String webDs) {
        return line.replaceAll(webDsRe, "MIYOUSHE_WEB_DS = \"" + webDs + "\"");
    }

    public static void replace(String version, String appDs, String webDs) throws IOException {
        if (version == null || appDs == null || webDs == null) {
            return;
        }
        if (version.isEmpty() || appDs.isEmpty() || webDs.isEmpty()) {
            return;
        }
        Path filePath = Paths.get(dsPy);
        List<String> lines = Files.readAllLines(filePath, StandardCharsets.UTF_8);
        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i);
            line = replaceVersion(line, version);
            line = replaceAppDs(line, appDs);
            line = replaceWebDs(line, webDs);
            lines.set(i, line);
        }
        Files.write(filePath, lines, StandardCharsets.UTF_8);
    }
}
